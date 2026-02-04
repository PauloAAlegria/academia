# este signals foi criado para apagar as imagens antigas da base de dados quando se insere uma imagem nova
# assim proporciona uma limpeza da base de dados e esta mantêm-se sempre leve porque não guarda dados antigos
import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from django.db.models import FileField
from django.conf import settings
import logging
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

# Lista de apps que suportam mídia (para limitar a aplicação dos sinais a apps específicos)
APPS_COM_SUPORTE_A_MEDIA = ['amdf', 'event', 'festival', 'polo', 'team']  # apenas modelos da apps


"""
Remove diretórios vazios acima do caminho do arquivo excluído,
até a pasta definida em 'stop_at' (por padrão, MEDIA_ROOT).
Isso evita que fiquem diretórios órfãos após remoção de arquivos.
"""
def delete_empty_parent_folders(path, stop_at=None):
    stop_at = stop_at or settings.MEDIA_ROOT
    stop_at = os.path.abspath(stop_at)
    dir_path = os.path.dirname(path)

    while dir_path.startswith(stop_at):
        try:
            os.rmdir(dir_path) # Só remove se estiver vazio
        except OSError:
            break # Sai do loop se o diretório não estiver vazio
        dir_path = os.path.dirname(dir_path)


"""
Exclui o arquivo físico se ele existir no sistema de arquivos,
e remove diretórios vazios acima dele.
"""
def delete_file(file_field):
    if file_field and hasattr(file_field, 'path') and os.path.isfile(file_field.path):
        path = file_field.path
        os.remove(path)
        delete_empty_parent_folders(path)


"""
Verifica se o mesmo arquivo está sendo usado por outra instância do mesmo modelo.
Isso evita apagar um arquivo ainda em uso por outro registro.
"""
def is_file_used_elsewhere(model_class, field_name, file_name, exclude_pk):
    lookup = {f"{field_name}": file_name}
    return model_class.objects.filter(**lookup).exclude(pk=exclude_pk).exists()


"""
Sinal executado antes de salvar uma instância.
Se um novo arquivo for enviado para substituir um antigo, e o antigo
não estiver sendo usado em outro lugar, ele será removido do sistema.
"""
@receiver(pre_save)
def auto_delete_old_file_on_change(sender, instance, **kwargs):
    # Aplica apenas aos modelos das apps autorizadas
    if sender._meta.app_label not in APPS_COM_SUPORTE_A_MEDIA:
        return
    # Se a instância for nova, não há nada a comparar
    if not instance.pk:
        return
    # Tenta obter a instância anterior (da base de dados)
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    # Percorre todos os campos do modelo
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)
            # Se o arquivo foi alterado, e o antigo não for usado em outro lugar
            if old_file and old_file != new_file:
                if not is_file_used_elsewhere(sender, field.name, old_file.name, instance.pk):
                    delete_file(old_file)


"""
Sinal executado após a exclusão de uma instância.
Remove todos os arquivos do tipo FileField, desde que o modelo
pertença a uma das apps autorizadas.
"""
@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if sender._meta.app_label not in APPS_COM_SUPORTE_A_MEDIA:
        return
    for field in instance._meta.fields:
        if isinstance(field, FileField):
            file = getattr(instance, field.name)
            delete_file(file)


"""
Intercepta tentativas de exclusão de users diretamente na base de dados (incluindo via terminal,
views, scripts ou mesmo pelo Admin), e impede que superusers sejam apagados.
"""
@receiver(pre_delete, sender=User)
def prevent_superuser_deletion(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied("Não é permitido excluir um superusuário!")


"""
Para registrar eventos suspeitos ou críticos no sistema
(como tentativa de alteração de segurança).
"""
logger = logging.getLogger(__name__)

@receiver(pre_delete, sender=User)
def prevent_superuser_deletion(sender, instance, **kwargs):
    if instance.is_superuser:
        logger.error(f"Tentativa de exclusão de superuser: {instance.username}")
        raise PermissionDenied("Não é permitido excluir um superuser!")
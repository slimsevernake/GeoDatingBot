from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)


from loader import dp, log


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        log.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        log.exception('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        log.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        log.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        log.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        log.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        log.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        log.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        log.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        log.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    
    log.exception(f'Update: {update} \n{exception}')

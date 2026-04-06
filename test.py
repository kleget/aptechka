from importt import *

@dp.message_handler(content_types=["audio"])
async def get_foto(message: types.Message):
    print(message.audio.file_id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
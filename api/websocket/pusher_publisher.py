import pusher


class PusherPublisher:
    def __init__(self):
        self.__instance = pusher.Pusher(
            app_id='1167312',
            key='33b4f28f7e51e14cc56f',
            secret='350309e2f8bacf2c793f',
            cluster='ap1',
            ssl=True
        )

    def publish_classifier_progress(self, task_id, percentage):
        self.__instance.trigger('upload', 'progress-' + task_id, {'percentage': percentage})

    def publish_lm_progress(self, percentage):
        self.__instance.trigger('upload', 'progress-lm', {'percentage': percentage})

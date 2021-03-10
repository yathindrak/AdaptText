import pusher


class Server:
    def __init__(self):
        self.instance = pusher.Pusher(
            app_id='1167312',
            key='33b4f28f7e51e14cc56f',
            secret='350309e2f8bacf2c793f',
            cluster='ap1',
            ssl=True
        )

    def publish(self, task_id, percentage):
        self.instance.trigger('upload', 'progress-'+task_id, {'percentage': percentage})

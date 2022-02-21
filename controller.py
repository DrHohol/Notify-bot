from db_models import Notifies, engine, sessionmaker
from datetime import datetime, timedelta

Session = sessionmaker(bind=engine)
session = Session()


class Controller:
    @staticmethod
    def create_notify(data):

        notify = Notifies(
            message_text=data["text"],
            reply_id=data["reply"],
            time=datetime.strptime(data["time"], "%d.%m.%y:%H.%M"),
            repeats=data["repeats"],
            chat_id=data["chat_id"],
        )
        session.add(notify)
        session.commit()

    @staticmethod
    def get_active():
        notifies = []
        notify = session.query(Notifies).all()
        # Little crutch
        # bcs filtering with datetime working bad
        for i in notify:
            if datetime.strftime(i.time, "%d.%m.%y:%H.%M") == datetime.strftime(
                datetime.utcnow(), "%d.%m.%y:%H.%M"
            ):
                notifies.append(
                    {
                        "text": i.message_text,
                        "reply_id": i.reply_id,
                        "chat_id": i.chat_id,
                    }
                )
                # If we have repeats
                # Bot will decrease it and set
                # Notify 10 minutes later
                if i.repeats != 0:
                    i.repeats -= 1
                    i.time = i.time + timedelta(minutes=10)
                else:
                    session.delete(i)
                session.commit()
        return notifies
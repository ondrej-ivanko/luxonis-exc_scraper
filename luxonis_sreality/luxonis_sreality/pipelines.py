# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from luxonis_sreality.db_engine import engine
from sqlalchemy.orm import sessionmaker
from luxonis_sreality.db_schema import AparmentsForSale


class LuxonisSrealityPipeline:
    def process_item(self, item, spider):
        self.db_session.add(AparmentsForSale(**item))
        try:
            self.db_session.commit()
        except Exception:
            self.db_session.rollback()
        finally:
            self.db_session.close()
        return item

    def open_spider(self, spider):
        Session = sessionmaker(bind=engine)
        self.db_session = Session()

    def close_spider(self, spider):
        try:
            self.db_session.close()
        except Exception:
            pass
        finally:
            engine.dispose()

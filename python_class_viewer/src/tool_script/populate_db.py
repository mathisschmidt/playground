from python_class_viewer.model.upload_info import UploadInfo
from python_class_viewer.services.database_manager import DatabaseManager

fake_data = [
    UploadInfo(
        file_name="sample.csv",
        file_size=150,
        number_class=2,
        number_methods=10,
        number_property=5,
        number_relation=1
    ),
    UploadInfo(
        file_name="analytics.py",
        file_size=300,
        number_class=5,
        number_methods=25,
        number_property=15,
        number_relation=4
    ),
    UploadInfo(
        file_name="data_processor.js",
        file_size=250,
        number_class=3,
        number_methods=18,
        number_property=8,
        number_relation=2
    ),
]

def clear_database():
    """Clear all records from the database."""

    deleted_count = UploadInfo.delete_all()
    print(f"Cleared {deleted_count} records from the database.")

def add_fake_datas() -> bool:
    for upload_info in fake_data:
        with DatabaseManager.get_session() as session:
            session.add(upload_info)
            session.commit()
    return True

if __name__ == "__main__":
    clear_database()
    success = add_fake_datas()
    if success:
        print("Database populated with fake data successfully.")
    else:
        print("Failed to populate database with fake data.")
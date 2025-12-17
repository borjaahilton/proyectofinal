import os
from app import create_app
from db import get_db

def revert_changes():
    app = create_app()
    with app.app_context():
        db = get_db()
        
        # 1. Update DB to point to the existing static image
        # Using root-relative path assuming Flask serves static at /static
        image_path = '/static/images/dunk_low.png'
        print(f"Updating products to use {image_path}...")
        
        # Update specific products I modified (1 and 14)
        # Or should I update all? The user said "return to how it was with a single image".
        # I'll update 1 and 14 for sure.
        db.execute("UPDATE productos SET imagen = %s WHERE id_producto IN (1, 14)", (image_path,))
        db.commit()
        
        # 2. Delete generated files
        static_folder = os.path.join(app.root_path, 'static')
        generated_files = [
            os.path.join(static_folder, 'img', 'products', 'product_1.png'),
            os.path.join(static_folder, 'img', 'products', 'product_14.png')
        ]
        
        print("Removing generated files...")
        for file_path in generated_files:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
            else:
                print(f"File not found (already deleted?): {file_path}")

        # Provide confirmation
        print("Revert complete.")

if __name__ == '__main__':
    revert_changes()

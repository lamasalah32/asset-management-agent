from sqlalchemy.orm import Session
import models, schemas

def create_asset(db: Session, asset: schemas.AssetCreate):
    db_asset = models.Asset(**asset.model_dump())
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_assets(db: Session):
    return db.query(models.Asset).all()

def get_asset(db: Session, asset_id: int):
    return db.query(models.Asset).filter(models.Asset.id == asset_id).first()

def update_asset(db: Session, asset_id: int, asset: schemas.AssetUpdate):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    for key, value in asset.model_dump().items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def delete_asset(db: Session, asset_id: int):
    db_asset = get_asset(db, asset_id)
    if not db_asset:
        return None
    db.delete(db_asset)
    db.commit()
    return db_asset


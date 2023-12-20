from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class coffeeshops(Base):
    __tablename__ = 'coffeeshops'
    nama_coffeeshop: Mapped[str] = mapped_column(primary_key=True)
    kualitas_kopi: Mapped[int] = mapped_column()
    pelayanan: Mapped[int] = mapped_column()
    lokasi: Mapped[int] = mapped_column()
    harga: Mapped[int] = mapped_column()
    wifi: Mapped[int] = mapped_column()
    
    def __repr__(self) -> str:
        return f"coffeeshops(nama_coffeeshop={self.nama_coffeeshop!r}, kualitas_kopi={self.kualitas_kopi!r})"
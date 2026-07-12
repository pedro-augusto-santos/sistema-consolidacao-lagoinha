from database import Base, engine
import models  # importa os models pra o SQLAlchemy "conhecer" as tabelas

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")
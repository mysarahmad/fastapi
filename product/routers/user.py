from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.params import Depends
from models import User
from schemas import SignUp,Login
from passlib.context import CryptContext
from models import get_db,pwd_context
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "a7c20eb6ac3257be5815785af70dcfc6bc828e1bfdba480b96c4d5e304a5cd6c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    print("************************************")
    print("inside the get current function !!!!!!")
    print("token",token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payload!!!",payload)
        email: str = payload.get("sub")
        print("email",email)

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise credentials_exception

    return user




router = APIRouter()

@router.get("/get_data")
def get_data(
    current_user: User = Depends(get_current_user)
):
    return current_user



@router.post("/signup")
def signup(requst : SignUp , db:Session = Depends(get_db)):
    try : 

        hashed_pass = pwd_context.hash(requst.password)
        data = User(name = requst.name , 
                    email = requst.email,
                    password = hashed_pass)
        
        db.add(data)
        db.commit()
        db.refresh(data)
        return data
    
    except Exception as e:
        return f"Error is ::: {e}"
    

    

@router.post("/login")
def login(request:Login,
          db:Session = Depends(get_db)):
    try:

        user = db.query(User).filter(User.email == request.email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="userName not found ")
        if not pwd_context.verify(request.password,
                                user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="password is incorrect")
            
        acess_token = generate_token(
            data = {"sub":request.email}
        )

        return {"acess_token":acess_token,
                "token_type":"bearer"}
    
    except Exception as e:
        return f"Error is ::: {e}"
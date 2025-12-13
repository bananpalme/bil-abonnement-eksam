from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from database import get_all_clients, get_cars, get_client_by_id, make_new_contract, get_all_contracts
from dotenv import load_dotenv
import os


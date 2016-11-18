#!/usr/bin/env python
# -*- coding: utf-8 -*

from xml.dom.minidom import parse
import tweepy #Librería para twitter.
#import bitlyapi #Librería para bitly.

class Twitt(object):
    def __init__(self):
        self.texto = None
        
    def initTwitt(self, pathXML):
        twitterDOM = parse(pathXML)
        twitterDOM = twitterDOM.documentElement.getElementsByTagName("twitter")[0]
        self.texto = twitterDOM.childNodes[0].data
        twitterDOM = twitterDOM.attributes
        self.caracteres = twitterDOM.get("caracteres").childNodes[0].data
        self.consumerKey = twitterDOM.get("CONSUMER_KEY").childNodes[0].data
        self.consumerSecret = twitterDOM.get("CONSUMER_SECRET").childNodes[0].data
        self.accessKey = twitterDOM.get("ACCESS_KEY").childNodes[0].data
        self.accessSecret = twitterDOM.get("ACCESS_SECRET").childNodes[0].data
        self.bitLyUsername = twitterDOM.get("BIT_LY_USERNAME").childNodes[0].data
        self.bitLyApiKey = twitterDOM.get("BIT_LY_API_KEY").childNodes[0].data
        
    def validarInicializarClase(self, pathXML):
        if (self.texto == None) and (pathXML != None):
            self.initTwitt(pathXML)
        elif (self.texto == None) and (pathXML == None):
            raise AttributeError("Falta path del XML")
            
    def getLimitChars(self):
        res = 0
        if self.texto != None:
            res = int(self.caracteres)
        return res
        
    def getTextoPredefinido(self):
        res = ""
        if self.texto != None:
            res = self.texto
        return res
    
    def setSugerenciaMsg(self, entrada):
        self.texto = self.texto.replace("\\titulo post y-o entradilla/", entrada)
    
    def conectarConTwitter(self, pathXML=None):
        # ESTE MÉTODO LANZA UNA EXCEPCIÓN SI NO SE CONECTA
        self.validarInicializarClase(pathXML)
        if (self.texto != None):
            auth = tweepy.OAuthHandler(self.consumerKey, self.consumerSecret)
            auth.set_access_token(self.accessKey, self.accessSecret)
            api = tweepy.API(auth)
        return auth, api
        
    def acortarLink(self, bigUrl, pathXML=None):
        self.validarInicializarClase(pathXML)
        if (self.texto != None):
            resultado = ""
            try:
                # Me conecto con mi usuario y clave a bit.ly
                b = bitlyapi.BitLy(self.bitLyUsername, self.bitLyApiKey)
                # Acorto la url del link
                res = b.shorten(longUrl=bigUrl)
                # Devuelvo la url acortada.
                resultado = res['url']
            except:
                resultado = bigUrl
        return resultado
        
    def enviarTuit(self, message, pathXML=None):
        # ESTE MÉTODO LANZA UNA EXCEPCIÓN SI NO SE CONECTA O NO PUEDE ENVIAR EL MENSAJE
        self.validarInicializarClase(pathXML)
        if (self.texto != None):
            auth, api = self.conectarConTwitter()
            api.update_status(message[0:int(self.caracteres)])



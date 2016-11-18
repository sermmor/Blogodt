#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gdata import service
import gdata
import atom
import blogger
from odf.odf2xhtml import ODF2XHTML

class odf2xhtmlWithoutError(ODF2XHTML):
    # Clase creada para que no de error en el constructor por el make_embedable
    def odf2xhtmlWithoutError(self):
        ODF2XHTML.__init__(self)
    
    def make_embedable(self):
        self.set_embedable()
    
class BloggerDesktopUtils(object):
    def BloggerDesktopUtils(self):
        self.service = None
        self.listBlogs = []
    
    def connectToBlogger(self, sUser, sPass):
        # Para el caso que no estemos conectados a blogger, que se conecte.
        self.service = blogger.login(sUser, sPass)
        self.createBlogList()
    
    def getConnection(self):
        return self.service
    
    def setConnection(self, newService):
        # Para el caso que ya estemos conectados a blogger, asignarle la misma conexión.
        self.service = newService
        self.createBlogList()
    
    def createBlogList(self):
        # @pre: self.service debe estar creado.
        # Añadir a las listas los blogs del servicio. Guardar los pares blogid y title en self.listBlogs.
        self.listBlogs = []
        for blogid, title in blogger.getblogs(self.service):
            self.listBlogs = self.listBlogs + [[blogid, title]]
    
    def getBlogList(self):
        return self.listBlogs
    

class DownloadBloggerToFileHTML(BloggerDesktopUtils):
    def DownloadBloggerToFileHTML(self):
        BloggerDesktopUtils.__init__(self)
        
    def getListPost(self, idBlog, iMaxNumPost, allDraft=None):
        # Si allDraft==True devolverá sólo los borradores, si es False caso las entradas que no sean borradores, en otro caso devuelve todo.
        query = service.Query() #Creamos una query.
        query.feed = '/feeds/' + idBlog + '/posts/default'
        query.max_results = iMaxNumPost

        feed = self.service.GetFeed(query.ToUri()) # Lanzo la query a la petición.
        #feed = self.service.Get('/feeds/' + idBlog + '/posts/default')
        misEntradas = []
        if allDraft != None:
            for post in feed.entry:
                if allDraft and blogger.is_draft(post):
                    misEntradas = misEntradas + [post]
                elif (not allDraft) and (not blogger.is_draft(post)):
                    misEntradas = misEntradas + [post]
        else:
            for post in feed.entry:
                misEntradas = misEntradas + [post]
        return misEntradas
    
    def saveHTMLPost(self, post, path, otherNameFile = None):
        def corregirTildes(sTextoHTML):
            # Minúsculas
            sNewTexto = sTextoHTML.replace("á", "&aacute;")
            sNewTexto = sNewTexto.replace("é", "&eacute;")
            sNewTexto = sNewTexto.replace("í", "&iacute;")
            sNewTexto = sNewTexto.replace("ó", "&oacute;")
            sNewTexto = sNewTexto.replace("ú", "&uacute;")
            sNewTexto = sNewTexto.replace("ñ", "&ntilde;")
            # Mayúsculas
            sNewTexto = sNewTexto.replace("Á", "&Aacute;")
            sNewTexto = sNewTexto.replace("É", "&Eacute;")
            sNewTexto = sNewTexto.replace("Í", "&Iacute;")
            sNewTexto = sNewTexto.replace("Ó", "&Oacute;")
            sNewTexto = sNewTexto.replace("Ú", "&Uacute;")
            sNewTexto = sNewTexto.replace("Ñ", "&Ntilde;")
            # Más símbolos
            sNewTexto = sNewTexto.replace("¿", "&iquest;")
            sNewTexto = sNewTexto.replace("—", "&#8212;")
            sNewTexto = sNewTexto.replace("¡", "&iexcl;")
            return sNewTexto
        # post está en el mismo formato que los elementos de la lista devuelve getListPost.
        title = "<Sin titulo>"
        content = ""
        if (post.content.text != None): 
            content = post.content.text
        if (otherNameFile != None):
            title = otherNameFile
        elif (post.title.text != None): 
            title = post.title.text
        preContent = "<html>\n <head>\n </head>\n<body>\n"
        postContent = "\n</body>\n</html>\n"
        content = corregirTildes(content)
        # Salvar en fichero .html
        title = title.replace("/", "-")
        title = title.replace("\\", "-")
        nomFile = path + "/" + post.updated.text   + " - " + title.decode('utf-8') + ".html"#).encode('utf-8')
        fich = open(nomFile, 'w')
        fich.write(preContent + "<h1>" + corregirTildes(title) + "</h1>\n" + content + postContent)
        fich.close()
        
class UploadOdtFileToBlogger(BloggerDesktopUtils):
    # No publicará directamente, la idea es que lo guarde como borrador, dé el enlace al borrador, y pueda añadir ya en el enlace las etiquetas y demás antes de darle a publicar. Así seguiré usando blogger pero será todo más sencillo gracias a poder subir odts.
    def UploadOdtFileToBlogger(self):
        BloggerDesktopUtils.__init__(self)
    
    def getStringHTMLOfODFDocument(self, pathFile, sEncode):
        generatecss = True 
        embedable = False 
        odhandler = odf2xhtmlWithoutError(generatecss, embedable) # Creo el manejador de odt
        result = odhandler.odf2xhtml(pathFile).encode(sEncode,'xmlcharrefreplace') # Creo el fichero HTML
        return result
        
    def updateBloggerWithHTMLText(self, sText, sTitle, idBlog):
        def adaptaABlog(texto):
            textoSplit = texto.split("\n")
            #defListEnterFusion = lambda str1, str2: str1 + "\n" + str2
            defListFusion = lambda str1, str2: str1 + str2
            preString = '''<style type="text/css">/*<![CDATA[*/'''
            iInitAll = 16
            iFinStyle = textoSplit.index("</style>")
            iInitBody = textoSplit.index("<body>")
            finalTexto = preString + reduce(defListFusion, textoSplit[iInitAll:iFinStyle]) + "</style>" + reduce(defListFusion, textoSplit[(iInitBody + 1):len(textoSplit)-3])
            return finalTexto
        # Guardar en borrador para posteriormente comprobar, añadir etiquetas y postear o programar.
        myNewEntry = blogger.create_entry(sTitle, adaptaABlog(sText), True)
        self.service.Post(myNewEntry, '/feeds/' + idBlog + '/posts/default')
        return myNewEntry
        
    def updateBloggerWithHTMLTextNotOdtExport(self, sText, sTitle, idBlog):
        def indexIgnoreCase(texto2, sSearch):
            # texto2 puede ser un String.
            indexEndHead = -1
            try:
                #Intento búsqueda normal.
                indexEndHead = texto2.index(sSearch)
            except:
                try:
                    #Intento búsqueda con todo en mayúsculas.
                    indexEndHead = texto2.upper().index(sSearch.upper())
                except:
                    #Intento búsqueda con todo en minúsculas.
                    indexEndHead = texto2.lower().index(sSearch.lower())
            # Si no lo encuentra de ninguna de las tres formas saltará una excepción, pero por lo que pueda pasar controlar lo del -1.
            return indexEndHead
        
        def adaptaABlog(texto):
            sInitBody = "<BODY LANG=\"es-ES\" DIR=\"LTR\">"
            finalTexto = texto
            iInitTexto = indexIgnoreCase(texto, sInitBody)
            if iInitTexto != -1:
                iInitTexto = iInitTexto + len(sInitBody)
                iFinalTexto = indexIgnoreCase(texto, "</BODY>")
                if iFinalTexto != -1:
                    finalTexto = texto[iInitTexto:iFinalTexto]
            return finalTexto
        
        # Guardar en borrador para posteriormente comprobar, añadir etiquetas y postear o programar.
        sStrangeSpace1 = '''<P STYLE="margin-bottom: 0cm"><BR> </P> '''
        sStrangeSpace2 = '''<P STYLE="margin-bottom: 0cm; font-style: normal"><BR> </P>'''
        #print "-------------------------------------------------------\n", sText.replace("\n", " "), "\n-------------------------------------------------------\n", sText.replace("\n", " ").replace(sStrangeSpace1, " ")
        myNewEntry = blogger.create_entry(sTitle, adaptaABlog(sText.replace("\n", " ").replace(sStrangeSpace1, "\n").replace(sStrangeSpace2, "\n")), True)
        self.service.Post(myNewEntry, '/feeds/' + idBlog + '/posts/default')
        return myNewEntry



import poppler, os.path, os, time, datetime
doc = poppler.document_new_from_file(path, None)

pages = [doc.get_page(i) for i in range(doc.get_n_pages())]

for page_no, page in enumerate(pages):
    items = [i.annot.get_contents() for i in page.get_annot_mapping()]
    items = [i for i in items if i]
    for j in items:
        # print "Found annotation: ... " + j 
        print path	
        j = j.replace("\r\n"," ")
        j = j.replace("\r\n"," ")
        x= x+"\n\n"+"'%s' (page %s)" % (j,page_no + 1)
        # print xk
        if "xk" in j:
            #xk= xk+"\n\n"+"'%s' (page %s)" % (j,page_no + 1)
            print j	
            g = open(myxkfolder+j+" "+lpath+" p. "+str(page_no)+'.txt', 'w')
            g.write(j)
            g.close()
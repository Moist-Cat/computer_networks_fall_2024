from tkinter import *
from tkinter import font
from tkinter import messagebox
from tooltip import CreateToolTip
from parse_http_url import parse_http_url,BadUrlError
from client import request,HTTPResponse

def get_text(widget):
    # Grab all the text ignoring the last eol
    return widget.get('1.0','end -1 c')

def parse_headers(rawHeaders):
    rawHeaders = rawHeaders.strip()
    lines = rawHeaders.split('\n')
    headers = {}
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        tmp = lines[i].split(':')
        # Error con array de tamano no 2
        if len(tmp) != 2:
            continue
        key = tmp[0].strip().lower()
        value = tmp[1].strip()
        headers.update({key: value})
    return headers

def make_request():
    method = methodVar.get()
    print(f"method='{method}'")
    
    rawUrl = get_text(urlView)
    (host,port,absPath,query) =  ("","","","")
    try:
        (host,port,absPath,query) = parse_http_url(rawUrl)
    except BadUrlError as e:
        messagebox.showerror("Error",message=e)
        return
    print(f"host='{host}'")
    print(f"port='{port}'")
    print(f"absPath='{absPath}'")
    print(f"query='{query}'")
    
    rawHeaders = get_text(headerView)
    headers = parse_headers(rawHeaders)
    print(f"headers='{headers}'")
    
    rawBody = get_text(bodyView)
    print(f"body='{rawBody}'")
    
    response: HTTPResponse = None
    try:
        response = request(method=method,url=rawUrl,headers=headers,body=rawBody)
    except Exception as e:
        messagebox.showerror("Error",message=f"An error ocurred during the request. {e}")
        return
    print(response)
    
    statusCodeVar.set(f"Status {response.code}")
    responseHeaderView.delete('1.0','end')
    responseHeaderView.insert('end',response.headers)
    responseBodyView.delete('1.0','end')
    responseBodyView.insert('end',response.body)

if __name__ == "__main__":
    window = Tk()
    window.title("PTTH Client")
    window.geometry("640x480")
    window.resizable(False,False)
    for i in range(12):
        window.columnconfigure(i,weight=2)
    window.columnconfigure((0,11),weight=1)
    
    # Request
    
    # METHOD SELECTION
    methods = ["OPTIONS","GET","HEAD","POST","PUT","DELETE","TRACE","CONNECT"]
    methodVar = StringVar(window)
    methodVar.set("GET")
    methodSelectionLabel = Label(window,text="Select a method")
    methodSelectionLabel.grid(column=1,row=0)
    methodSelectionView = OptionMenu(window,methodVar,"GET",*methods)
    methodSelectionView.grid(column=1,row=1,sticky="nsew")
    
    # URL Field
    urlLabel = Label(window,text="Provide an URL")
    urlLabel.grid(column=3,row=0,columnspan=8)
    urlView = Text(window,height=1,width=1)
    urlView.grid(column=3,row=1,sticky="nsew",columnspan=8)
    
    # Headers field
    headerLabel = Label(window,text="Provide headers")
    underlineFont = font.Font(headerLabel,headerLabel.cget("font"))
    underlineFont.configure(underline=True)
    headerLabel.configure(font=underlineFont)
    headerLabel.grid(column=1,row=2,sticky="nsew",columnspan=3)
    CreateToolTip(headerLabel,text="Provide headers one per line as key:value pairs\nExample\n\ncontent-type:text/html\ncache-control:private\ncontent-encoding:gzip")
    headerView = Text(window,width=2,height=5)
    headerView.grid(column=1,row=3,sticky="nsew",columnspan=3)
    
    # Body
    bodyLabel = Label(window,text="Provide body")
    bodyLabel.grid(column=4,row=2,columnspan=7,sticky="nsew",padx=5)
    bodyView = Text(window,width=2,height=5)
    bodyView.grid(column=4,row=3,columnspan=7,sticky="nsew",padx=5)
    
    # Make request
    requestButton = Button(window,text="Send Request",command=make_request)
    requestButton.grid(row=4,column=1,columnspan=2,sticky="nsew",pady=5)
    
    # Response 
    responseSectionLabel = Label(window,text="Response")
    responseSectionLabel.grid(row=5,column=3,sticky="nsew")
    

    # Status
    statusCodeVar = StringVar(window)
    statusCodeVar.set("Status NA")
    responseStatusLabel = Label(window,textvariable=statusCodeVar)
    responseStatusLabel.grid(row=5,column=5,sticky="nsew")
    
    # Headers
    responseHeaderLabel = Label(window,text="Response headers")
    responseHeaderLabel.grid(column=1,row=6,sticky="nsew",columnspan=3)
    responseHeaderView = Text(window,width=2,height=5)
    responseHeaderView.grid(column=1,row=7,sticky="nsew",columnspan=3)
    
    # Body
    responseBodyLabel = Label(window,text="Provide body")
    responseBodyLabel.grid(column=4,row=6,columnspan=7,sticky="nsew",padx=5)
    responseBodyView = Text(window,width=2,height=5)
    responseBodyView.grid(column=4,row=7,columnspan=7,sticky="nsew",padx=5)
    
    # Body
    window.mainloop()
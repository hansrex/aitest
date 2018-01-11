function createXMLHttpRequest() {  
    var xmlHttp;  
    if (window.XMLHttpRequest) {  
        xmlHttp = new XMLHttpRequest();  
        if (xmlHttp.overrideMimeType)  
            xmlHttp.overrideMimeType('text/xml');  
    } else if (window.ActiveXObject) {  
        try {  
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");  
        } catch (e) {  
            try {  
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");  
            } catch (e) {  
            }  
        }  
    }  
    return xmlHttp;  
}


function postProject(project)  
{  
    var xmlHttp = createXMLHttpRequest();   
    var url = "127.0.0.1:8080/receive";  
    xmlHttp.open("POST", url, true);  
    xmlHttp.onreadystatechange = getStatusBack;  
    xmlHttp.setRequestHeader("Content-Type",  "application/x-www-form-urlencoded;");  
    xmlHttp.send(project);  
}

postProject("")
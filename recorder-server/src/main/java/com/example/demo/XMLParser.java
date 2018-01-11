package com.example.demo;
import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.util.regex.*;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import com.google.gson.*;
import java.util.UUID;

public class XMLParser {

    private String cleanData;
    public XMLParser(String rawData){
       this.cleanData = cleanRawData(rawData);
    }

    private String cleanRawData(String rawData){
        String pattern = "<input.*?>";
        Pattern reg = Pattern.compile(pattern);
        Matcher maches = reg.matcher(rawData);
        if(maches.find()){
            rawData = rawData + "</input>";
            return rawData;
        }
        return "";
    }

    private Document loadXML() {

        Document xmlDoc = null;
        DocumentBuilderFactory builderFactory = DocumentBuilderFactory.newInstance();
        try {
            InputStream is = new ByteArrayInputStream(this.cleanData.getBytes());
            DocumentBuilder builder = builderFactory.newDocumentBuilder();
            xmlDoc = builder.parse(is);
            return xmlDoc;
        } catch(ParserConfigurationException e) {
            e.printStackTrace();
            return xmlDoc;
        } catch(SAXException e) {
            e.printStackTrace();
            return xmlDoc;
        } catch(IOException e) {
            e.printStackTrace();
            return xmlDoc;
        }
    }

    public String getJsonData() {

        List<RecordData> datas = new ArrayList<>();
        Map<String, List<RecordData>> oneSenario = new HashMap<>();
        Document xmlDoc = loadXML();
        Gson gson = new Gson();
        try{
            if(xmlDoc != null) {
                XPath xpath = XPathFactory.newInstance().newXPath();
                NodeList nodeList = (NodeList)xpath.evaluate("input/tr", xmlDoc, XPathConstants.NODESET);
                if(nodeList.getLength() != 0) {
                    for(int i = 0; i < nodeList.getLength(); i++) {
                        RecordData oneData = new RecordData();
                        String id = (String)xpath.evaluate("@id", nodeList.item(i), XPathConstants.STRING);
                        oneData.setId(id);
                        NodeList nodeList1= nodeList.item(i).getChildNodes();
                        if(nodeList1.getLength() == 3){
                            String command = nodeList1.item(0).getChildNodes().item(0).getTextContent();
                            oneData.setCommand(command);
                            String target = nodeList1.item(1).getChildNodes().item(0).getTextContent();
                            oneData.setTarget(target);
                            String value = nodeList1.item(2).getChildNodes().item(0).getTextContent();
                            oneData.setValue(value);
                            NodeList options = nodeList1.item(1).getLastChild().getChildNodes();
                            List<String> optionList = new ArrayList<>();
                            for(int j = 0; j < options.getLength(); j++){
                                optionList.add(options.item(j).getTextContent());
                            }
                            oneData.setOptions(optionList);
                        }
                        datas.add(oneData);
                    }
                }
                oneSenario.put(UUID.randomUUID().toString(),datas);
                return gson.toJson(oneSenario);
            }

            return gson.toJson(oneSenario);

        } catch(XPathExpressionException e) {
            e.printStackTrace();
            return gson.toJson(oneSenario);
        }
    }
}

package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Logger;

@RestController
public class HelloController {

    private final Logger logger = Logger.getLogger(getClass().toString());
    @Value("${spring.data.mongodb.uri}")
    private String address;
    private final DBHandler db = new DBHandler(address);
//    @Autowired
//    private DiscoveryClient client;

    @RequestMapping(value = "/receive", method = RequestMethod.POST, produces = "application/json; charset=utf-8")
    public String receive(@RequestBody String project){
        XMLParser parser = new XMLParser(project);
        String projectJson = parser.getJsonData();
        String result = db.insertRecord(projectJson);
        return result;
    }
}

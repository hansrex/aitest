package com.example.demo;
import java.util.ArrayList;
import java.util.List;

import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.MongoCredential;
import com.mongodb.ServerAddress;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

public class DBHandler {

    private MongoDatabase mongoDatabase;

    private MongoCollection<Document> collection;

    public DBHandler(String address){
        this.connectDB(address);
    }

    private void connectDB(String address){
        try {
            ServerAddress serverAddress = new ServerAddress(address, 27088);
            List<ServerAddress> addrs = new ArrayList<ServerAddress>();
            addrs.add(serverAddress);

            MongoCredential credential = MongoCredential.createScramSha1Credential("record", "recorddb", "123456".toCharArray());
            List<MongoCredential> credentials = new ArrayList<>();
            MongoClient mongoClient = new MongoClient(addrs, credentials);
            this.mongoDatabase = mongoClient.getDatabase("recorddb");
            this.collection = this.mongoDatabase.getCollection("datas");
        }catch (Exception e){
            System.out.print(e);
        }
    }

    public String insertRecord(String record){
        try {
            Document oneRecord = Document.parse(record);
            this.collection.insertOne(oneRecord);
            return "{code:1}";
        }catch (Exception e){
            return "{code:0}";
        }
    }
}

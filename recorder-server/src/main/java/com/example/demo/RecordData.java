package com.example.demo;

import java.util.ArrayList;
import java.util.List;

public class RecordData {
    private String id;
    private String command;
    private String target;
    private String value;
    private List<String> options;

    public RecordData(){
        this.id = "";
        this.command = "";
        this.target = "";
        this.value = "";
        this.options = new ArrayList<>();
    }

    public void setId(String value){
        this.id = value;
    }
    public void setCommand(String value){
        this.command = value;
    }

    public void setTarget(String value){
        this.target = value;
    }

    public void setValue(String value){
        this.value = value;
    }

    public void setOptions(List<String> value){
        this.options = value;
    }

    public String getId(){
        return this.id;
    }

    public String getCommand(){
        return this.command;
    }

    public String getTarget() {
        return this.target;
    }

    public String getValue() {
        return  this.value;
    }

    public List<String> getOptions() {
        return this.options;
    }
}

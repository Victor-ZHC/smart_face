package com.example.wy.facerecognition;

import org.apache.http.HttpException;

public class UploadResponse {
    String url;

    //get filename
    public String parseUrl() throws HttpException{
        String prefix_before = "http://10.225.226.39:5000/images/";
        String prefix = "http://localhost:5000/images/";

        if (url==null)
            throw new HttpException("Url is null");
        if (!url.startsWith(prefix))
            throw new HttpException("Url is wrong");

        return url.substring(prefix.length());
    }

}
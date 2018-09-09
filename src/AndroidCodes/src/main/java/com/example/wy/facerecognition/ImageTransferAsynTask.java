package com.example.wy.facerecognition;

import android.app.Activity;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.View;
import android.widget.ImageView;

import java.io.File;
import java.io.InputStream;

import org.apache.http.HttpEntity;
import org.apache.http.HttpException;
import org.apache.http.HttpResponse;
import org.apache.http.HttpStatus;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.mime.HttpMultipartMode;
import org.apache.http.entity.mime.MultipartEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.apache.http.entity.mime.content.FileBody;

import com.google.gson.Gson;

public class ImageTransferAsynTask implements Runnable{

    private File outputImage;
    private ImageView picture;
    private ImageView waiting;

    private Activity activity;

    public ImageTransferAsynTask(File file,ImageView picture,ImageView waiting,Activity activity){
        outputImage = file;
        this.picture=picture;
        this.waiting=waiting;
        this.activity =activity;
    }

    @Override
    public void run() {
        //simple try connection
        simpleTryGet();

        //上传到服务器  重新显示标注的照片
        String fileName = ImageTransferAsynTask.uploadImage(outputImage);

        final Bitmap bitmap_taged = ImageTransferAsynTask.requestTagedImage(fileName);

        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                picture.setImageBitmap(bitmap_taged);
                waiting.setVisibility(View.INVISIBLE);
            }
        });
    }

    //simple connection try
    public static void simpleTryGet() {
        try {

            HttpClient httpClient = new DefaultHttpClient();
            HttpGet httpGet = new HttpGet("http://10.0.2.2:5000/api/random");

            HttpResponse response = httpClient.execute(httpGet);
            HttpEntity resEntity = response.getEntity();


            if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
                HttpEntity httpEntity = response.getEntity();

                final String responseStr = EntityUtils.toString(resEntity)
                        .trim();
                System.out.println("SimpleTryGet function returns "+responseStr);

                //httpGet.releaseConnection();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    //receive url of image
    public static String uploadImage(File image) {
        String fileName = null;
        try {

            //simple connection try

            HttpClient httpClient = new DefaultHttpClient();
            HttpPost httpPost = new HttpPost("http://10.0.2.2:5000/upload");

            FileBody fileBody = new FileBody(image);
            MultipartEntity reqEntity = new MultipartEntity(HttpMultipartMode.BROWSER_COMPATIBLE);
            reqEntity.addPart("file", fileBody);


            httpPost.setEntity(reqEntity);

            HttpResponse response = httpClient.execute(httpPost);
            HttpEntity resEntity = response.getEntity();

            if (resEntity != null) {
                final String responseStr = EntityUtils.toString(resEntity)
                        .trim();
                System.out.println(responseStr);
                UploadResponse uploadResponse = new Gson().fromJson(responseStr, UploadResponse.class);
                fileName = uploadResponse.parseUrl();
            } else {
                throw new HttpException("No returned message");
            }
            //httpPost.releaseConnection();

        } catch (Exception e) {
            e.printStackTrace();
        }

        return fileName;
    }

    //receive taged image
    public static Bitmap requestTagedImage(String url) {
        try {

            HttpClient httpClient = new DefaultHttpClient();
            HttpGet httpGet = new HttpGet("http://10.0.2.2:5000/images/"+url);

            HttpResponse response = httpClient.execute(httpGet);
            HttpEntity resEntity = response.getEntity();


            if (response.getStatusLine().getStatusCode() == HttpStatus.SC_OK) {
                HttpEntity httpEntity = response.getEntity();

                // 获得一个输入流
                InputStream is = httpEntity.getContent();

                //图片转换为bitmap格式
                Bitmap bitmap = BitmapFactory.decodeStream(is);


               // httpGet.releaseConnection();
                return bitmap;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println();
        return null;
    }


}
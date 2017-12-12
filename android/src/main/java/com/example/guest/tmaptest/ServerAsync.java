package com.example.guest.tmaptest;

import android.os.AsyncTask;
import android.util.Log;
import android.widget.TextView;

import com.skp.Tmap.TMapView;

import org.w3c.dom.Text;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.BufferedWriter;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URL;

/**
 * Created by hoyong on 2017-08-09.
 */

public class ServerAsync extends AsyncTask<String, String, Void> {

    TextView textView;
    TMapView tmapView;
    public String res;
    private BufferedReader networkReader;
    private BufferedWriter networkWriter;
    Socket s = null;

    public ServerAsync(TextView textView) {
        this.textView = textView;
    }

    @Override
    protected void onProgressUpdate(String... values) {
        //txtView_receive.setText(values[0]);
        super.onProgressUpdate(values);
        ((MainActivity)MainActivity.context).setTextView(res);
    }

    @Override
    protected Void doInBackground(String... strings) {
        try {
            if(s == null){
                try{
                    s = new Socket("192.168.43.132", 8888);
                      networkWriter = new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));
                      networkReader = new BufferedReader(new InputStreamReader(s.getInputStream()));
                }catch(Exception e){
                    Log.i("socket","connection error");
                }

            }

            /*read*/
            while(true) {
                Log.w("Chatting is running", "chatting is running");
                char[] recStr = new char[1024];
                int rec = 0;
                int i =0;
                while(rec != '#') {
                    rec = networkReader.read();
                    recStr[i++] = (char)rec;

                }
                recStr[--i] = '\0';
                res = new String(recStr,0,i);
                publishProgress();
                Log.i("tcp test", res);


            }

            /*write

            while(true) {
                Log.w("Chatting is running", "chatting is running");
                    String a = "보내고 싶어...문자를.";
                    networkWriter.write(a);
            }

            */
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
}

package com.example.guest.tmaptest;

/**
 * Created by gaeun on 2017. 10. ..
 */

import android.Manifest;
import android.annotation.TargetApi;
import android.app.Activity;
import android.app.Application;
import android.app.PendingIntent;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.IntentFilter;
import android.graphics.Color;
import android.os.Build;
import android.speech.tts.TextToSpeech;
import android.telephony.SmsManager;
import android.text.method.ScrollingMovementMethod;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.LinearLayout;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.speech.RecognizerIntent;
import android.location.Location;
import com.skp.Tmap.TMapGpsManager;
import com.skp.Tmap.*;
import com.skp.Tmap.TMapCircle;

import org.w3c.dom.Text;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;

public class MainActivity extends AppCompatActivity
        implements TMapGpsManager.onLocationChangedCallback{

    ServerAsync sa;
    private TMapView tMapView = null;
    private TMapGpsManager tMapGps = null;
    private TMapData tMapData = null;
    private TMapPathData tMapPathData = null;

    private static final int REQUEST_CODE = 1;
    private Button rcvData;
    private TextView Speech;
    private static String apiKey = "1210b3f5-5e42-3356-8f54-d10a83aeebc2";
    private boolean m_bTrackingMode, m_WalkingMode;
    private int point_idx = 0;
    ArrayList<String> matches_text;
    TMapPoint startpoint;
    TextToSpeech tts;
    static TextView textView, directionView;
    public static Context context;
    String destination;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Speech = (TextView) findViewById(R.id.textView2) ;
        LinearLayout mapView = (LinearLayout) findViewById(R.id.mapview);
        textView = (TextView) findViewById(R.id.textView);
        rcvData = (Button) findViewById(R.id.rcvData);
        directionView = (TextView) findViewById(R.id.directionView);
        context = this;
        tMapView = new TMapView(this);
        tMapGps = new TMapGpsManager(MainActivity.this);
        tMapData = new TMapData();

        m_WalkingMode = false;
        m_bTrackingMode = false;

        textView.setMovementMethod(new ScrollingMovementMethod());

        tts=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if (status != TextToSpeech.ERROR) {
                    tts.setLanguage(Locale.KOREAN);
                }
            }
        });

        setTmapView();
        setGpsManager();
        mapView.addView(tMapView);

        startpoint = new TMapPoint(tMapView.getCenterPoint().getLatitude(),tMapView.getCenterPoint().getLongitude());

        rcvData.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                //살리기 --- textView.setText("direction : "+sa.res);
                tMapView.setCompassMode(true);
                tMapView.setTrackingMode(true);
                tMapView.setSightVisible(true);


               // textView.append(Double.toString(startpoint.getLatitude()) +" ,,,, "+Double.toString(startpoint.getLongitude()) );
            }
        });
    }


    public void setGpsManager(){
        getPermission();
        //tMapGps.setProvider(tMapGps.NETWORK_PROVIDER);  // 인터넷 이용 - 실내 전용
        tMapGps.setProvider(tMapGps.GPS_PROVIDER);    // gps이용
        tMapGps.setMinTime(0);
        tMapGps.setMinDistance(0);
        tMapGps.OpenGps();
    }

    public void getPermission(){
        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_COARSE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            if (!ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.ACCESS_COARSE_LOCATION)) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                        1);
            }
        }

        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            if (!ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.ACCESS_FINE_LOCATION)) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                        1);
            }
        }

        if (ContextCompat.checkSelfPermission(this,
                Manifest.permission.SEND_SMS)
                != PackageManager.PERMISSION_GRANTED) {
            if (!ActivityCompat.shouldShowRequestPermissionRationale(this,
                    Manifest.permission.SEND_SMS)) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.SEND_SMS},
                        1);
            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(tts !=null){
            tts.stop();
            tts.shutdown();
        }
    }

    public void setTmapView(){
        tMapView.setSKPMapApiKey(apiKey);
        tMapView.setCompassMode(true);
        tMapView.setIconVisibility(true);
        tMapView.setZoomLevel(30);
        tMapView.setMapType(TMapView.MAPTYPE_STANDARD);
        tMapView.setLanguage(TMapView.LANGUAGE_KOREAN);
        tMapView.setTrackingMode(true);
        tMapView.setSightVisible(true);
    }

    @Override
    public void onLocationChange(Location location) {

        tMapView.setLocationPoint(location.getLongitude(),location.getLatitude());
        startpoint.setLatitude(location.getLatitude());
        startpoint.setLongitude(location.getLongitude());

        // 디버깅용
        TMapCircle circle = new TMapCircle();
        circle.longitude = location.getLongitude();
        circle.latitude = location.getLatitude();
        circle.setRadius(2);
        circle.setAreaColor(Color.BLUE);
        tMapView.addTMapCircle("dd",circle);

        if(!m_bTrackingMode){
            tMapView.setLocationPoint(location.getLongitude(),location.getLatitude());
            TextToSpeech("목적지");
            SpeechToText();
            m_bTrackingMode = true;
        }
        else if(m_WalkingMode ){
            textView.setText(point_idx+"번째 point \n");

            /* 다음 경로 안내 */
            if(tMapPathData.getDistance(startpoint, tMapPathData.pathPoints.get(point_idx)) <= 5 ) {
                try {


                    textView.append("5 미만 : " + Double.toString(tMapPathData.getDistance(startpoint, tMapPathData.pathPoints.get(point_idx))) + "\n");

                    if (point_idx > 0) {
                        double preDir = tMapPathData.directions.get(point_idx - 1);
                        double postDir = tMapPathData.directions.get(point_idx);
                        double drctDif = preDir - postDir;

                        if (drctDif > 180) drctDif = drctDif - 360;
                        else if (drctDif < -180) drctDif = drctDif + 360;
                        textView.append(Double.toString(drctDif) + "\n");


                        //location.getBearing()
                /* 오른쪽 회전 처리 */
                        if (drctDif < -45 && drctDif > -100) {
                            textView.append("오른쪽\n");
                            TextToSpeech("우측으로 가세요");
                        } else if (drctDif > 45 && drctDif < 100) {
                            textView.append("왼쪽\n");
                            TextToSpeech("좌측으로 가세요");
                        }
                    }

                    point_idx++;
                }
                catch (Exception e){
                    TextToSpeech("목적지 부근 입니다");

                }
            }
            /* 그 이외의 경우 */
//            else{
//
//                //textView.append("10 넘음 : " + Double.toString(tMapPathData.getDistance(startpoint, tMapPathData.pathPoints.get(point_idx))) + "\n");
//                /* 경로로부터 직교거리 20m 이상 멀어지는 경우, 새로운 경로 탐색 */
//                if (tMapPathData.getDistance(
//                        startpoint,
//                        tMapPathData.GetOrthogonalPoint(tMapPathData.pathPoints.get(point_idx),
//                                tMapPathData.pathPoints.get(point_idx+1), startpoint)) > 20) {
//
//                    addText("직선거리 20 넘음 : "+Double.toString(tMapPathData.getDistance(
//                            startpoint,
//                            tMapPathData.GetOrthogonalPoint(tMapPathData.pathPoints.get(point_idx),
//                                    tMapPathData.pathPoints.get(point_idx+1), startpoint)))+"\n");
//
//                    TextToSpeech("새로 안내");
//                }
//            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {

        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            matches_text = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            destination = matches_text.get(0);
            Speech.setText(destination);
            tMapPathData = new TMapPathData(startpoint,destination,tMapView,getApplicationContext());
            tMapPathData.execute();

            sa = new ServerAsync(directionView);
            sa.executeOnExecutor(tMapPathData.THREAD_POOL_EXECUTOR);

            //나중에 살리기
            TextToSpeech(destination);
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    public void addText(String text) {
        textView.append(text);
    }

    public boolean findpath(){
        m_WalkingMode = true;
        point_idx = 0;
        return true;
    }

    public void setTextView(String string){
            directionView.setText(string);
    }

    public void TextToSpeech(String text) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            ttsGreater21(text);
        } else {
            ttsUnder20(text);
        }
    }

    @SuppressWarnings("deprecation")
    private void ttsUnder20(String text) {
        HashMap<String, String> map = new HashMap<>();
        map.put(TextToSpeech.Engine.KEY_PARAM_UTTERANCE_ID, "MessageId");
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, map);
    }

    @TargetApi(Build.VERSION_CODES.LOLLIPOP)
    private void ttsGreater21(String text) {
        String utteranceId=this.hashCode() + "";
        tts.speak(text, TextToSpeech.QUEUE_FLUSH, null, utteranceId);
    }

    public void SpeechToText(){

        if (isConnected()) {
            Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                    RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
            startActivityForResult(intent, REQUEST_CODE);
        } else {
            Toast.makeText(getApplicationContext(), "Please Connect to Internet", Toast.LENGTH_LONG).show();
        }
    }

    public boolean isConnected()
    {
        ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo net = cm.getActiveNetworkInfo();
        if (net!=null && net.isAvailable() && net.isConnected()) {
            return true;
        } else {
            return false;
        }
    }
}


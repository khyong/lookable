package com.example.guest.tmaptest;

import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.app.Activity;
import android.telephony.SmsManager;
import android.view.GestureDetector;
import android.view.GestureDetector.OnGestureListener;
import android.view.MotionEvent;
import android.widget.Toast;

public class HomeActivity extends Activity implements OnGestureListener {

    private static final int SWIPE_MIN_DISTANCE = 120;  //스와이프 했을때 최소 거리
    private static final int SWIPE_MAX_OFF_PATH = 250;  //스와이프 했을때 최대 거리
    private static final int SWIPE_THRESHOLD_VELOCITY = 200; // 스와이프 인식시 속도
    private GestureDetector gestureScanner;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        gestureScanner = new GestureDetector(this);
        setContentView(R.layout.activity_home);
    }

    @Override
    public boolean onTouchEvent(MotionEvent me) {
        return gestureScanner.onTouchEvent(me);
    }

    public boolean onDown(MotionEvent e) {

        return true;
    }

    public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
        try {
            if (Math.abs(e1.getY() - e2.getY()) > SWIPE_MAX_OFF_PATH)
                return false;
            // right to left swipe
            if (e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE
                    && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                Toast.makeText(getApplicationContext(), "경로 안내 모드",
                        Toast.LENGTH_SHORT).show();
                Intent intent = new Intent(this, MainActivity.class);
                startActivity(intent);

            }
            // left to right swipe
            else if (e2.getX() - e1.getX() > SWIPE_MIN_DISTANCE
                    && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                Toast.makeText(getApplicationContext(), "Right Swipe",
                        Toast.LENGTH_SHORT).show();
                sendSMS("01051873983", "LOOKable Monitoring WebSite \n http://13.125.11.55:8080/  ");
            }
//            // down to up swipe
//            else if (e1.getY() - e2.getY() > SWIPE_MIN_DISTANCE
//                    && Math.abs(velocityY) > SWIPE_THRESHOLD_VELOCITY) {
//                Toast.makeText(getApplicationContext(), "Swipe up",
//                        Toast.LENGTH_SHORT).show();
//            }
//            // up to down swipe
//            else if (e2.getY() - e1.getY() > SWIPE_MIN_DISTANCE
//                    && Math.abs(velocityY) > SWIPE_THRESHOLD_VELOCITY) {
//                Toast.makeText(getApplicationContext(), "Swipe down",
//                        Toast.LENGTH_SHORT).show();
//            }
        } catch (Exception e) {
        }

        return true;
    }

    public void onLongPress(MotionEvent e) {

    }

    public boolean onScroll(MotionEvent e1, MotionEvent e2, float distanceX, float distanceY) {
        return true;
    }

    public void onShowPress(MotionEvent e) {
    }

    public boolean onSingleTapUp(MotionEvent e) {
        return true;
    }

    public void sendSMS(String Number, String message){
        String SENT = "SMS_SENT";
        String DELIVERED = "SMS_DELIVERED";

        PendingIntent sentPI = PendingIntent.getBroadcast(this,0, new Intent(SENT),0);
        PendingIntent deliveredPI = PendingIntent.getBroadcast(this,0,new Intent(DELIVERED),0);

        registerReceiver(new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                switch (getResultCode()) {
                    case Activity.RESULT_OK:
                        Toast.makeText(getBaseContext(), "문자 전송 성공", Toast.LENGTH_SHORT).show();
                        break;
                }

            }
        },new IntentFilter(SENT));

        SmsManager sms = SmsManager.getDefault();
        sms.sendTextMessage(Number, null, message, sentPI, deliveredPI);

    }
}

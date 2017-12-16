package com.example.guest.tmaptest;

import com.skp.Tmap.TMapCircle;
import com.skp.Tmap.TMapData;
import com.skp.Tmap.TMapPOIItem;
import com.skp.Tmap.TMapPoint;
import com.skp.Tmap.TMapPolyLine;
import com.skp.Tmap.TMapView;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.util.Log;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Created by gaeun on 2017. 11. 29..
 */

public class TMapPathData extends AsyncTask<String,Boolean,Boolean> implements Serializable {
    TMapData tMapPathData = new TMapData();
    TMapPoint StartPoint, EndPoint;
    TMapPOIItem item;
    TMapView tMapView;
    String destination;
    ArrayList<TMapPOIItem> tMapPOIItems;
    ArrayList<Double> directions = new ArrayList<Double>();
    ArrayList<Double> distances = new ArrayList<Double>();
    ArrayList<TMapPoint> pathPoints = new ArrayList<TMapPoint>();

    public TMapPathData(TMapPoint StartPoint, String destination, TMapView tMapView, Context context) {
        this.StartPoint = StartPoint;
        this.destination = destination;
        this.tMapView = tMapView;
        this.EndPoint = new TMapPoint(0,0);
    }

    @Override
    protected Boolean doInBackground(String... strings) {

        try {

            tMapPOIItems = tMapPathData.findAroundKeywordPOI(StartPoint, destination, 2, 20);

            item = tMapPOIItems.get(0);
            this.EndPoint.setLatitude(item.getPOIPoint().getLatitude());
            this.EndPoint.setLongitude(item.getPOIPoint().getLongitude());

            tMapPathData.findPathDataWithType(TMapData.TMapPathType.PEDESTRIAN_PATH ,StartPoint, EndPoint, new TMapData.FindPathDataListenerCallback() {
                @Override
                public void onFindPathData(TMapPolyLine polyLine) {
                    polyLine.setLineWidth(10);
                    Log.i("width",Float.toString(polyLine.getLineWidth()));
                    tMapView.addTMapPath(polyLine);
                    pathPoints = polyLine.getLinePoint();

                    for(int i=0; i<pathPoints.size(); i++){
                            TMapCircle c = new TMapCircle();
                            c.latitude = pathPoints.get(i).getLatitude();
                            c.longitude = pathPoints.get(i).getLongitude();
                            c.setRadius(2);
                            tMapView.addTMapCircle(Integer.toString(i),c);
                    }

                    for(int i=1; i<pathPoints.size(); i++) {
                            Double direction = bearingP1toP2(pathPoints.get(i - 1), pathPoints.get(i));
                            Double distance = getDistance(pathPoints.get(i - 1), pathPoints.get(i));

                            if (direction >= 0) {
                                directions.add(direction);
                                distances.add(distance);
                                Log.i("directions", i + " : " + direction + "    distances:" + distance);
                            }
                    }
                    publishProgress(true);
                }
            });

            return true;

        } catch(Exception e){
            Log.i("aaaa","async catch");
            e.printStackTrace();
        }
        return false;
    }

    @Override
    protected void onProgressUpdate(Boolean... progress) {
        ((MainActivity)MainActivity.context).findpath();
    }

    @Override
    protected void onPostExecute(Boolean result){

        Log.i("PostExecute",Boolean.toString(result));
        if(result==true){
            boolean chk =false;
        }
    }

    public double bearingP1toP2(TMapPoint p1, TMapPoint p2)
    {
        double P1_latitude = p1.getLatitude();
        double P1_longitude= p1.getLongitude();
        double P2_latitude = p2.getLatitude();
        double P2_longitude = p2.getLongitude();

        // 현재 위치 : 위도나 경도는 지구 중심을 기반으로 하는 각도이기 때문에 라디안 각도로 변환한다.
        double Cur_Lat_radian = P1_latitude * (3.141592 / 180);
        double Cur_Lon_radian = P1_longitude * (3.141592 / 180);
        // 목표 위치 : 위도나 경도는 지구 중심을 기반으로 하는 각도이기 때문에 라디안 각도로 변환한다.
        double Dest_Lat_radian = P2_latitude * (3.141592 / 180);
        double Dest_Lon_radian = P2_longitude * (3.141592 / 180);
        // radian distance
        double radian_distance = 0;
        radian_distance = Math.acos(Math.sin(Cur_Lat_radian) * Math.sin(Dest_Lat_radian) + Math.cos(Cur_Lat_radian) * Math.cos(Dest_Lat_radian) * Math.cos(Cur_Lon_radian - Dest_Lon_radian));

        // 목적지 이동 방향을 구한다.(현재 좌표에서 다음 좌표로 이동하기 위해서는 방향을 설정해야 한다. 라디안값이다.
        double radian_bearing = Math.acos((Math.sin(Dest_Lat_radian) - Math.sin(Cur_Lat_radian) * Math.cos(radian_distance)) / (Math.cos(Cur_Lat_radian) * Math.sin(radian_distance)));        // acos의 인수로 주어지는 x는 360분법의 각도가 아닌 radian(호도)값이다.
        double true_bearing = 0;
        if (Math.sin(Dest_Lon_radian - Cur_Lon_radian) < 0) {
            true_bearing = radian_bearing * (180 / 3.141592);
            true_bearing = 360 - true_bearing;
        }
        else {
            true_bearing = radian_bearing * (180 / 3.141592);
        }

        return true_bearing;
    }

    public double getDistance(TMapPoint p1, TMapPoint p2) {

        double lon1 = p1.getLongitude();
        double lat1 = p1.getLatitude();
        double lon2 = p2.getLongitude();
        double lat2 = p2.getLatitude();

        double theta = lon1 - lon2;
        double dist = Math.sin(deg2rad(lat1)) * Math.sin(deg2rad(lat2)) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.cos(deg2rad(theta));

        dist = Math.acos(dist);
        dist = rad2deg(dist);
        dist = dist * 60 * 1.1515;
        dist = dist * 1609.344;

        return (dist);
    }

    private static double deg2rad(double deg) {
        return (deg * Math.PI / 180.0);
    }

    private static double rad2deg(double rad) {
        return (rad * 180 / Math.PI);
    }

    public TMapPoint GetOrthogonalPoint(TMapPoint start, TMapPoint end, TMapPoint target) {

        double xx = 0.0;
        double yy = 0.0;

        if(start.getLatitude() == end.getLatitude()) {
            xx = start.getLatitude();
            yy = target.getLongitude();
        }
        else if (start.getLongitude() == end.getLongitude()) {
            xx = target.getLatitude();
            yy = start.getLongitude();
        }
        else {
            double m1 = (end.getLongitude() - start.getLongitude())/(end.getLatitude() - start.getLatitude());
            double k1 = -m1 * start.getLatitude() + start.getLongitude();

            double m2 = -1 / m1;
            double k2 = - m2 * target.getLatitude() + target.getLongitude();

            xx = (k2-k1) / (m1 - m2);
            yy = m1 * xx + k1;
        }

        TMapPoint returnCrd = new TMapPoint(xx, yy);
        return returnCrd;
    }

}

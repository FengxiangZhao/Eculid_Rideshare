package com.example.b.rideshare;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Geocoder;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapFragment;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.IOException;

public class ResultMapActivity extends AppCompatActivity implements OnMapReadyCallback {
    private GoogleMap mMap;
    private TextView tripInfo;

    private LatLngBounds.Builder llbuilder = new LatLngBounds.Builder();
    private double originLat, originLon, destLat, destLon;
    private String TAG = "Result Map";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_result_map);
        tripInfo = (TextView) findViewById(R.id.scheduled_departure_TIME);
        originLat = getIntent().getExtras().getDouble("originLat");
        originLon = getIntent().getExtras().getDouble("originLon");
        destLat = getIntent().getExtras().getDouble("destLat");
        destLon = getIntent().getExtras().getDouble("destLon");
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);

    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap) {
        mMap = googleMap;
        Log.i(TAG, Double.toString(originLat) + ":" + Double.toString(originLon) + ":" + Double.toString(destLat) + ":" + Double.toString(destLon));
        Geocoder geocoder = new Geocoder(ResultMapActivity.this);
        String origName = "", destName = "";
        try {
//            Log.i(TAG,geocoder.getFromLocation(originLat,originLon,1).get(0).getAddressLine(0));
            origName = geocoder.getFromLocation(originLat, originLon, 1).get(0).getAddressLine(0);
            destName = geocoder.getFromLocation(destLat, destLon, 1).get(0).getAddressLine(0);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (IndexOutOfBoundsException e) {
            origName = Double.toString(originLat) + Double.toString(originLon);
            destName = Double.toString(destLat) + Double.toString(destLon);

        }
        LatLng orig = new LatLng(originLat, originLon);
        LatLng dest = new LatLng(destLat, destLon);
        llbuilder.include(orig);
        llbuilder.include(dest);
        LatLngBounds bounds = llbuilder.build();
        mMap.addMarker(new MarkerOptions().position(orig));
        mMap.addMarker(new MarkerOptions().position(dest));
        mMap.moveCamera(CameraUpdateFactory.newLatLngBounds(bounds, 165));
        String tripinfo = getIntent().getExtras().getString("time");
        String matchInfo = getIntent().getExtras().getString("match");
        if (tripinfo.contains("Unmatched"))
            tripInfo.setText("From: " + origName + "\nTo: " + destName + "\n" + tripinfo);

        else {
            if (tripinfo.contains("[Matched]Driver")) { //is driver
                StringBuilder driversb = new StringBuilder();
                for (int i = 1; i < matchInfo.split("\"username\"").length; i++) {
                    driversb.append(matchInfo.split("\"email\"")[i].split(",")[0] + "(").append(matchInfo.split("\"phone\"")[i].split(",")[0]).append(")\n");
                }
                tripInfo.setText("From: " + origName + "\nTo: " + destName + "\nRole: " + tripinfo + "\nMatched Rider: " + driversb.toString().replace("\"","").replace(":",""));
            }
            else {
                StringBuilder driversb = new StringBuilder();
                for (int i = 1; i < matchInfo.split("\"username\"").length; i++) {
                    driversb.append(matchInfo.split("\"email\"")[i].split(".edu")[0]).append(".edu(").append(matchInfo.split("\"phone\"")[i].split("\",")[0]).append(")\n");
                }
                tripInfo.setText("From: " + origName + "\nTo: " + destName + "\nRole: " + tripinfo + "\nMatched \n" + driversb.toString().replace("\"","").replace(":",""));
            }

        }

        //mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(41.506491, -81.606372), 12)); //Location of CWRU

    }


}

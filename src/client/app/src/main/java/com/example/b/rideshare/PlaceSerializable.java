package com.example.b.rideshare;

import android.util.Log;

import com.google.android.gms.location.places.Place;

import java.io.Serializable;
import java.text.DecimalFormat;

public class PlaceSerializable implements Serializable {


    CharSequence address;
    String latitude,longitude;

    public PlaceSerializable(Place p) {
        DecimalFormat df = new DecimalFormat("00.0000000");
        address = p.getAddress();
        latitude =  df.format(p.getLatLng().latitude);
        Log.i("place: ", "Str lat: " + latitude);
        Log.i("place: ", "parse lat: " + df.format(p.getLatLng().latitude));

        longitude = df.format(p.getLatLng().longitude);
        Log.i("place: ", "Str lont " + longitude);
        Log.i("place: ", "parse  lont: " + df.format(p.getLatLng().longitude));


    }

    public CharSequence getAddress() {
        return address;
    }

    public String getLatitude() {
        return latitude;
    }

    public String getLongitude() {
        return longitude;
    }
}

package com.example.b.rideshare;

import com.google.android.gms.location.places.Place;

import java.io.Serializable;

public class PlaceSerializable implements Serializable {


    CharSequence address;
    double latitude,longitude;

    public PlaceSerializable(Place p) {
        address = p.getAddress();
        latitude =  p.getLatLng().latitude;
        longitude = p.getLatLng().longitude;
    }

    public CharSequence getAddress() {
        return address;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }
}

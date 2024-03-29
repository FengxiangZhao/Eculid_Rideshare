package com.example.b.rideshare;

import android.Manifest;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.gms.common.GooglePlayServicesNotAvailableException;
import com.google.android.gms.common.GooglePlayServicesRepairableException;
import com.google.android.gms.common.api.Status;
import com.google.android.gms.location.places.Place;
import com.google.android.gms.location.places.ui.PlaceAutocomplete;
import com.google.android.gms.location.places.ui.PlaceAutocompleteFragment;
import com.google.android.gms.location.places.ui.PlaceSelectionListener;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.LatLngBounds;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.maps.model.Polyline;
import com.google.android.gms.maps.model.PolylineOptions;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;


public class MapsActivity2 extends AppCompatActivity implements
        OnMapReadyCallback, GoogleMap.OnMyLocationButtonClickListener,
        GoogleMap.OnMyLocationClickListener, ActivityCompat.OnRequestPermissionsResultCallback {

    private GoogleMap mMap;
    private boolean mPermissionDenied = false;
    private View mMapView;
    private int PLACE_AUTOCOMPLETE_REQUEST_CODE = 1;
    private boolean fromEntered = false;
    private boolean toEntered = false;
    private Place from, to;
    private String token;
    private LocationManager locationManager;
    private LatLngBounds.Builder llbuilder = new LatLngBounds.Builder();
    private Marker fromMarker,toMarker;
    private Polyline myPolyline;
    private Boolean isVerified;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps2);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager()
                .findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
        mMapView = mapFragment.getView();

        PlaceAutocompleteFragment autocompleteFragment = (PlaceAutocompleteFragment)
                getFragmentManager().findFragmentById(R.id.place_autocomplete_fragment);
        token = getIntent().getExtras().getString("token");

        Log.i("token", token);
        verifiyUser();

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

        // Add a marker in Sydney and move the camera

        mMap.setOnMyLocationButtonClickListener(this);
        mMap.setOnMyLocationClickListener(this);
     //   enableMyLocation();
        mMap.moveCamera(CameraUpdateFactory.newLatLngZoom(new LatLng(41.506491, -81.606372), 12)); //Location of CWRU

    }

    /**
     * Enables the My Location layer if the fine location permission has been granted.
     */
    private void enableMyLocation() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
                != PackageManager.PERMISSION_GRANTED) {
            // Permission to access the location is missing.
            PermissionUtils.requestPermission(this, 1,
                    Manifest.permission.ACCESS_FINE_LOCATION, true);
        } else if (mMap != null) {
            // Access to the location has been granted to the app.
            mMap.setMyLocationEnabled(true);
            View locationButton = ((View) mMapView.findViewById(Integer.parseInt("1")).getParent()).findViewById(Integer.parseInt("2"));
            RelativeLayout.LayoutParams rlp = (RelativeLayout.LayoutParams) locationButton.getLayoutParams();
// position on right bottom
            rlp.addRule(RelativeLayout.ALIGN_PARENT_TOP, 0);
            rlp.addRule(RelativeLayout.ALIGN_PARENT_BOTTOM, RelativeLayout.TRUE);
            rlp.setMargins(0, 0, 30, 110);


        }


    }


    @Override
    public boolean onMyLocationButtonClick() {
        //Toast.makeText(this, "MyLocation button clicked", Toast.LENGTH_SHORT).show();
        locationManager = (LocationManager) getSystemService(MapsActivity2.LOCATION_SERVICE);
     //   if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            Location myLocation = locationManager.getLastKnownLocation(LocationManager.PASSIVE_PROVIDER);
            Log.i("maps","currentLoc: " + myLocation.getLatitude() + ";" + myLocation.getLongitude());
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.

    //    }
        // Return false so that we don't consume the event and the default behavior still occurs
        // (the camera animates to the user's current position).
        return false;
    }

    @Override
    public void onMyLocationClick(@NonNull Location location) {
        Toast.makeText(this, "Current location:\n" + location, Toast.LENGTH_LONG).show();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        if (requestCode != 1) {
            return;
        }

        if (PermissionUtils.isPermissionGranted(permissions, grantResults,
                Manifest.permission.ACCESS_FINE_LOCATION)) {
            // Enable the my location layer if the permission has been granted.
            enableMyLocation();
        } else {
            // Display the missing permission error dialog when the fragments resume.
            mPermissionDenied = true;
        }
    }

    @Override
    protected void onResumeFragments() {
        super.onResumeFragments();
        if (mPermissionDenied) {
            // Permission was not granted, display error dialog.
            showMissingPermissionError();
            mPermissionDenied = false;
        }
    }

    /**
     * Displays a dialog with error message explaining that the location permission is missing.
     */
    private void showMissingPermissionError() {
        PermissionUtils.PermissionDeniedDialog
                .newInstance(true).show(getSupportFragmentManager(), "dialog");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu,menu); //fetch menu objects
        return true; // allow menu to show
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.id_my_trips:
                Intent intent = new Intent(MapsActivity2.this, ResultActivity.class);
                intent.putExtra("token", token);
                startActivity(intent);
                break;
            case R.id.id_about:
                showNormalDialog("About","1.0");
                break;
            case R.id.id_my_profiles:
                intent = new Intent(MapsActivity2.this, ProfileActivity.class);
                intent.putExtra("token", token);
                startActivity(intent);
                break;
            default:
                break;

        }
        return true;
    }


    private void showNormalDialog(String title, String message){
        final AlertDialog.Builder normalDialog =
                new AlertDialog.Builder(MapsActivity2.this);
        normalDialog.setTitle(title);
        normalDialog.setMessage(message);
        normalDialog.setNegativeButton("OK",
                new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        //...To-do
                    }
                });
        normalDialog.show();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == 1 || requestCode == 2) {
            if (resultCode == RESULT_OK) {
                TextView tv;
                Place place = PlaceAutocomplete.getPlace(this, data);
                llbuilder = new LatLngBounds.Builder();


                if (requestCode == 1) { //if it is pickup
                    Log.i("autocomplete", "pickup recieved ");
                    tv = (TextView) findViewById(R.id.pickup);
                    toEntered = true;
                    from = place;
                    MarkerOptions markerOptions = new MarkerOptions();
                    markerOptions.position(place.getLatLng());
                    markerOptions.title(place.getLatLng().latitude + " : " + place.getLatLng().longitude);
                    //mMap.clear();
                    if (fromMarker != null)
                     fromMarker.remove();
                    fromMarker = mMap.addMarker(markerOptions);
                    llbuilder.include(fromMarker.getPosition());
                    if (toMarker != null)
                        llbuilder.include(toMarker.getPosition());
                    LatLngBounds bounds = llbuilder.build();
                    if (toMarker != null) {
                        mMap.animateCamera(CameraUpdateFactory.newLatLngBounds(bounds, 135));
                      //  mMap.animateCamera(CameraUpdateFactory.zoomOut());
                    }
                    else {
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(fromMarker.getPosition(), 14.0f));
                    }

                } else { //if it is dropoff
                    Log.i("autocomplete", "dropoff recieved ");
                    tv = (TextView) findViewById(R.id.drop);
                    fromEntered = true;
                    to = place;
                    MarkerOptions markerOptions = new MarkerOptions();
                    markerOptions.position(place.getLatLng());
                    markerOptions.title(place.getLatLng().latitude + " : " + place.getLatLng().longitude);
                    if (toMarker != null)
                    toMarker.remove();
                    toMarker = mMap.addMarker(markerOptions);
                    llbuilder.include(toMarker.getPosition());
                    if (fromMarker != null)
                        llbuilder.include(fromMarker.getPosition());
                    LatLngBounds bounds = llbuilder.build();
                    if (fromMarker != null) {
                        mMap.animateCamera(CameraUpdateFactory.newLatLngBounds(bounds, 135));
                       // mMap.animateCamera(CameraUpdateFactory.zoomOut());
                    }
                    else {
                        mMap.animateCamera(CameraUpdateFactory.newLatLngZoom(toMarker.getPosition(), 14.0f));
                    }

                }

                if (fromMarker != null && toMarker != null) {
                    PolylineOptions polylineOptions = new PolylineOptions();
                    polylineOptions.color( Color.parseColor( "#CC0000FF" ) );
                    polylineOptions.width( 5 );
                    polylineOptions.visible( true );
                    polylineOptions.add(toMarker.getPosition());
                    polylineOptions.add(fromMarker.getPosition());
                    if (myPolyline != null)
                        myPolyline.remove();
                   // myPolyline = mMap.addPolyline(polylineOptions);
                }
                tv.setText(place.getAddress());
                //assign the textview forecolor
                tv.setTextColor(Color.RED);
                enableNextButton();
                Log.i("autocomplete", "Place: " + place.getName());
            } else if (resultCode == PlaceAutocomplete.RESULT_ERROR) {
                Status status = PlaceAutocomplete.getStatus(this, data);
                // TODO: Handle the error.
                Log.i("autocomplete", status.getStatusMessage());

            } else if (resultCode == RESULT_CANCELED) {
                // The user canceled the operation.
            }
        }
    }

    public void set_pickup(View v)
    {



        try {
            Intent intent =
                    new PlaceAutocomplete.IntentBuilder(PlaceAutocomplete.MODE_OVERLAY)
                            .build(this);
            intent.putExtra("type","pickup");
            startActivityForResult(intent, 1);
        } catch (GooglePlayServicesRepairableException e) {
            // TODO: Handle the error.
        } catch (GooglePlayServicesNotAvailableException e) {
            // TODO: Handle the error.
        }



    }


    public void set_drop(View v)
    {


        try {
            Intent intent =
                    new PlaceAutocomplete.IntentBuilder(PlaceAutocomplete.MODE_OVERLAY)
                            .build(this);
            intent.putExtra("type","drop");
            startActivityForResult(intent, 2);
        } catch (GooglePlayServicesRepairableException e) {
            // TODO: Handle the error.
        } catch (GooglePlayServicesNotAvailableException e) {
            // TODO: Handle the error.
        }

    }


    public void goNext(View v) {
        Button b = (Button)findViewById(R.id.next);
        Intent intent = new Intent(MapsActivity2.this, postActivity.class);
        intent.putExtra("from",new PlaceSerializable(from));
        intent.putExtra("to",new PlaceSerializable(to));
        intent.putExtra("token",token);
        startActivityForResult(intent, 1);

    }

    private void verifiyUser() {
        isVerified = false;
        RequestQueue requestQueue = Volley.newRequestQueue(MapsActivity2.this);
        String url ="https://api.extrasmisc.com/account/";
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, url, new JSONObject(), new com.android.volley.Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                Log.i("login","success");
                Log.i("login","response:" + response.toString());
                try {
                     if (response.getString("is_email_verified").contains("true")) {
                         isVerified = true;
                         Log.i("verifyemail","email Verified");
                     } else {
                         showNormalDialog("Email Unverified","Your email is unverified until you click the verification link in the welcome message that is sent to you when you create your account.You won't be able to post trips until your account is verified.");
                         Button nextButton = (Button)findViewById(R.id.next);
                         nextButton.setText("email unverified");
                     }
                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }

        }, new com.android.volley.Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.i("login",error.networkResponse.headers.toString());
                Toast toast = Toast.makeText(MapsActivity2.this, "Unable to log in with provided credentials.", Toast.LENGTH_SHORT);
                toast.show();

            }
        }) {
            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String>  params = new HashMap<String, String>();
                params.put("Content-Type","application/json");
                params.put("Authorization","JWT " + token);
                return params;
            }
        };

        requestQueue.add(jsonObjectRequest);
    }

    private void enableNextButton() {
        if (toEntered && fromEntered && isVerified) {
            Button nextButton = (Button)findViewById(R.id.next);
            nextButton.setEnabled(true);
        }


    }





}

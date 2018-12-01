package com.example.b.rideshare;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.annotation.TargetApi;
import android.app.DatePickerDialog;
import android.app.TimePickerDialog;
import android.support.v7.app.AppCompatActivity;
import android.app.LoaderManager.LoaderCallbacks;

import android.content.CursorLoader;
import android.content.Loader;
import android.database.Cursor;
import android.net.Uri;
import android.os.AsyncTask;

import android.os.Build;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.text.Editable;
import android.text.TextWatcher;
import android.util.Log;
import android.view.KeyEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.inputmethod.EditorInfo;
import android.widget.ArrayAdapter;
import android.widget.AutoCompleteTextView;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.NumberPicker;
import android.widget.TextView;
import android.widget.TimePicker;
import android.widget.Toast;
import android.widget.ToggleButton;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TimeZone;

/**
 * A login screen that offers login via email/password.
 */
public class postActivity extends AppCompatActivity implements LoaderCallbacks<Cursor>, NumberPicker.OnValueChangeListener, DatePickerDialog.OnDateSetListener, TimePickerDialog.OnTimeSetListener {

    /**
     * Id to identity READ_CONTACTS permission request.
     */
    private static final int REQUEST_READ_CONTACTS = 0;

    /**
     * A dummy authentication store containing known user names and passwords.
     * TODO: remove after connecting to a real authentication system.
     */
    private static final String[] DUMMY_CREDENTIALS = new String[]{
            "foo@example.com:hello", "bar@example.com:world"
    };
    /**
     * Keep track of the login task to ensure we can cancel it if requested.
     */
    private UserLoginTask mAuthTask = null;

    // UI references.
    private AutoCompleteTextView fromView;
    private EditText toView,seat,date,time,time_waiting,time_sharing;
    private View mProgressView;
    private View mLoginFormView;
    private PlaceSerializable from, to;
    private String token;
    boolean isDriver = true;
    private Button post_find_button;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_post);
        from = (PlaceSerializable) getIntent().getSerializableExtra("from");
        to = (PlaceSerializable) getIntent().getSerializableExtra("to");
        post_find_button = findViewById(R.id.email_sign_in_button);

        // Set up the login form.
        fromView = (AutoCompleteTextView) findViewById(R.id.from);
        fromView.setText(from.getAddress());
        fromView.setEnabled(false);

        toView = (EditText) findViewById(R.id.to);
        toView.setText(to.getAddress());
        toView.setEnabled(false);
        //     dp_init();
        token = getIntent().getExtras().getString("token");


        toView.setOnEditorActionListener(new TextView.OnEditorActionListener() {
            @Override
            public boolean onEditorAction(TextView textView, int id, KeyEvent keyEvent) {
                if (id == EditorInfo.IME_ACTION_DONE || id == EditorInfo.IME_NULL) {
                    attemptPost();
                    return true;
                }
                return false;
            }
        });

        Button mEmailSignInButton = (Button) findViewById(R.id.email_sign_in_button);
        mEmailSignInButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                if (isDriver)
                    attemptPost();
                else
                    attemptFind();
            }
        });

        mLoginFormView = findViewById(R.id.login_form);
        mProgressView = findViewById(R.id.login_progress);


        seat = findViewById(R.id.seat_num);
        date = findViewById(R.id.date_edittext);
        time = findViewById(R.id.time_edittext);
        time_waiting = findViewById(R.id.time_timewaiting);
        time_sharing = findViewById(R.id.time_sharing);
        time_sharing.setHint("driver_time_constraint_in_minute");


        ((EditText) findViewById(R.id.seat_num)).addTextChangedListener(new TextWatcher() {
            @Override
            public void beforeTextChanged(CharSequence s, int start, int count, int after) {

            }

            @Override
            public void onTextChanged(CharSequence s, int start, int before, int count) {
                if (count > 0 && (Integer.parseInt(s.toString()) < 1 || Integer.parseInt(s.toString()) > 7))
                    ((EditText) ((EditText) findViewById(R.id.seat_num))).setError("seats can be only 1-7");
                else
                    ((EditText) ((EditText) findViewById(R.id.seat_num))).setError(null);
            }

            @Override
            public void afterTextChanged(Editable s) {
            }
        });

        ((ToggleButton)findViewById(R.id.toggleButton)).setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked) {
                    Log.i("post", "switch to passenger");
                    time_sharing.setVisibility(View.INVISIBLE);
                    time_sharing.setHint("");
                    isDriver = false;
                    post_find_button.setText("Find");
                } else {
                    Log.i("post", "switch to driver");
                    time_sharing.setVisibility(View.VISIBLE);
                    time_sharing.setHint("driver_time_constraint_in_minute");
                    post_find_button.setText("Post");
                    isDriver = true;
                }
            }
        });

    }


    private boolean checkInput() {
        boolean isLegal = true;
        if (date.getText().toString().equals("")) {
            date.setError("please enter the date of departure");
            isLegal = false;
        }

        if (time.getText().toString().equals("")) {
            time.setError("please enter the time of departure");
            isLegal = false;
        }

        if (seat.getText().toString().equals("")) {
            seat.setError("please enter the seats available for sharing");
            isLegal = false;
        }

        if (time_waiting.getText().toString().equals("")) {
            time_waiting.setError("please enter the flexibility of the time of your departure");
            isLegal = false;
        }

        if (isDriver && time_sharing.getText().toString().equals("")) {
            time_sharing.setError("please enter the extra time you are willing to use for your trip");
            isLegal = false;
        }


        return isLegal;

    }


    /**
     * Attempts to sign in or register the account specified by the login form.
     * If there are form errors (invalid email, missing fields, etc.), the
     * errors are presented and no actual login attempt is made.
     */
    private void attemptPost() {


        //if all inputs are legal
        if (checkInput()) {
            Log.i("post", "Start auth");
            HashMap data = new HashMap();
            data.put("origin_lon",from.getLongitude());
            data.put("origin_lat",from.getLatitude());
            data.put("destination_lon",to.getLongitude());
            data.put("destination_lat",to.getLatitude());
            Log.i("post","origin_lon:" + from.getLongitude());
            Log.i("post","origin_lat:" + from.getLatitude());
            Log.i("post","destination_lon:" + to.getLongitude());
            Log.i("post","destination_lat:" + to.getLatitude());

            data.put("car_capacity",seat.getText().toString());
            data.put("scheduled_departure_datetime",date.getText().toString() + "T" + time.getText().toString() + ":00Z");
            Log.i("post","scheduled_departure_datetime:" + date.getText().toString() + "T" + time.getText().toString() + ":00Z");
            data.put("scheduled_departure_time_range_in_minute",time_waiting.getText().toString());
            data.put("driver_time_constraint_in_minute",time_sharing.getText().toString());


            String url = "https://api.extrasmisc.com/driver/";

            RequestQueue requestQueue = Volley.newRequestQueue(postActivity.this);

            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, new JSONObject(data), new com.android.volley.Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    Log.i("post", "success");
                    Log.i("post", response.toString());
                    Toast.makeText(postActivity.this, "Success!", Toast.LENGTH_SHORT).show();
                    finish();
                    //  Intent intent = new Intent(LoginActivity.this, MapsActivity2.class);
                    //    intent.putExtra("token",response.getString("token"));
                    // startActivity(intent);
                }

            }, new com.android.volley.Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.i("post", new String(error.networkResponse.data));
                    Toast toast = Toast.makeText(postActivity.this, "Unable to post", Toast.LENGTH_SHORT);
                    toast.show();

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    Map<String, String> params = new HashMap<String, String>();
                    params.put("Content-Type", "application/json");
                    params.put("Authorization", "JWT " + token);
                    return params;
                }
            };

            requestQueue.add(jsonObjectRequest);

        }
    }

    private void attemptFind() {


        //if all inputs are legal
        if (checkInput()) {
            Log.i("post", "Start auth");
            String url = "https://api.extrasmisc.com/driver/";
            RequestQueue requestQueue = Volley.newRequestQueue(postActivity.this);
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET, url, new JSONObject(), new com.android.volley.Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    Log.i("post", "success");
                    Log.i("post", response.toString());
                    try {
                        Log.i("post",response.getString("origin_lon"));
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }

                    Toast.makeText(postActivity.this, "Success!", Toast.LENGTH_SHORT).show();
                   // finish();
                    //  Intent intent = new Intent(LoginActivity.this, MapsActivity2.class);
                    //    intent.putExtra("token",response.getString("token"));
                    // startActivity(intent);
                }

            }, new com.android.volley.Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    Log.i("post", error.getMessage());
                    String response = error.getMessage();
                    String[] jsonString = response.split("\\},");
                    JsonParser parser = new JsonParser();
                    ArrayList<JsonObject> jsonObjects = new ArrayList();
                    for (String s: jsonString) {
                        s = s + "}";
                        JsonObject o = parser.parse(s).getAsJsonObject();
                        jsonObjects.add(o);
                        Log.i("post","json: " + s);
                    }

                    for (JsonObject jo: jsonObjects) {
                        Log.i("post","id " + jo.get("id").getAsString());
                    }



                    Toast toast = Toast.makeText(postActivity.this, "Unable to find", Toast.LENGTH_SHORT);
                    toast.show();

                }
            }) {
                @Override
                public Map<String, String> getHeaders() throws AuthFailureError {
                    Map<String, String> params = new HashMap<String, String>();
                    params.put("Content-Type", "application/json");
                    params.put("Authorization", "JWT " + token);
                    return params;
                }
            };

            requestQueue.add(jsonObjectRequest);

        }
    }


    /**
     * Shows the progress UI and hides the login form.
     */
    @TargetApi(Build.VERSION_CODES.HONEYCOMB_MR2)
    private void showProgress(final boolean show) {
        // On Honeycomb MR2 we have the ViewPropertyAnimator APIs, which allow
        // for very easy animations. If available, use these APIs to fade-in
        // the progress spinner.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.HONEYCOMB_MR2) {
            int shortAnimTime = getResources().getInteger(android.R.integer.config_shortAnimTime);

            mLoginFormView.setVisibility(show ? View.GONE : View.VISIBLE);
            mLoginFormView.animate().setDuration(shortAnimTime).alpha(
                    show ? 0 : 1).setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    mLoginFormView.setVisibility(show ? View.GONE : View.VISIBLE);
                }
            });

            mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
            mProgressView.animate().setDuration(shortAnimTime).alpha(
                    show ? 1 : 0).setListener(new AnimatorListenerAdapter() {
                @Override
                public void onAnimationEnd(Animator animation) {
                    mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
                }
            });
        } else {
            // The ViewPropertyAnimator APIs are not available, so simply show
            // and hide the relevant UI components.
            mProgressView.setVisibility(show ? View.VISIBLE : View.GONE);
            mLoginFormView.setVisibility(show ? View.GONE : View.VISIBLE);
        }
    }

    @Override
    public void onValueChange(NumberPicker picker, int oldVal, int newVal) {
//        ((EditText)findViewById(R.id.seat_num)).setText(newVal);
    }

    @Override
    public Loader<Cursor> onCreateLoader(int i, Bundle bundle) {
        return new CursorLoader(this,
                // Retrieve data rows for the device user's 'profile' contact.
                Uri.withAppendedPath(ContactsContract.Profile.CONTENT_URI,
                        ContactsContract.Contacts.Data.CONTENT_DIRECTORY), ProfileQuery.PROJECTION,

                // Select only email addresses.
                ContactsContract.Contacts.Data.MIMETYPE +
                        " = ?", new String[]{ContactsContract.CommonDataKinds.Email
                .CONTENT_ITEM_TYPE},

                // Show primary email addresses first. Note that there won't be
                // a primary email address if the user hasn't specified one.
                ContactsContract.Contacts.Data.IS_PRIMARY + " DESC");
    }

    @Override
    public void onLoadFinished(Loader<Cursor> cursorLoader, Cursor cursor) {
        List<String> emails = new ArrayList<>();
        cursor.moveToFirst();
        while (!cursor.isAfterLast()) {
            emails.add(cursor.getString(ProfileQuery.ADDRESS));
            cursor.moveToNext();
        }

        addEmailsToAutoComplete(emails);
    }

    @Override
    public void onLoaderReset(Loader<Cursor> cursorLoader) {

    }

    private void addEmailsToAutoComplete(List<String> emailAddressCollection) {
        //Create adapter to tell the AutoCompleteTextView what to show in its dropdown list.
        ArrayAdapter<String> adapter =
                new ArrayAdapter<>(postActivity.this,
                        android.R.layout.simple_dropdown_item_1line, emailAddressCollection);

        fromView.setAdapter(adapter);
    }

    public void changeDate(View v) {
        Calendar calendar = Calendar.getInstance(TimeZone.getDefault());
        calendar.setTimeInMillis(System.currentTimeMillis());
        Date date = new Date();
        DatePickerDialog dialog = new DatePickerDialog(postActivity.this, this, date.getYear(), date.getMonth(), date.getDate());
        //disable past date
        dialog.getDatePicker().setMinDate(System.currentTimeMillis() - 1000);
        dialog.show();
    }

    public void changeTime(View v) {
        Calendar calendar = Calendar.getInstance(TimeZone.getDefault());
        calendar.setTimeInMillis(System.currentTimeMillis());
        Date date = new Date();
        //set theme as 3 as the THEME_HOLO_LIGHT
        TimePickerDialog dialog = new TimePickerDialog(postActivity.this, 3, this, date.getHours(), date.getMinutes(), true);
        dialog.show();
    }

    @Override
    public void onDateSet(DatePicker view, int year, int month, int dayOfMonth) {
        String monthFormatted,dateFormatted;
        Log.i("post","year:" + year + " month:" + month + " dayOfMonth:" + dayOfMonth);
        if (month < 9) {
            monthFormatted = "0" + (month + 1);
        } else {
            monthFormatted = String.valueOf(month + 1);
        }

        if (dayOfMonth < 10) {
            dateFormatted = "0" + dayOfMonth;
        } else {
            dateFormatted = String.valueOf(dayOfMonth);
        }

        Log.i("post","date set as: " + "" + year + "-" + monthFormatted + "-" + dateFormatted);
        date.setText(Integer.toString(year) + "-" + monthFormatted + "-" + dateFormatted);
    }

    @Override
    public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
        EditText time = (EditText) findViewById(R.id.time_edittext);
        String minuteFormatted;
        if (minute < 10) {
            minuteFormatted = "0" + minute;
        } else {
            minuteFormatted = String.valueOf(minute);
        }
        time.setText(String.valueOf("" + hourOfDay + ":" + minuteFormatted));
    }


    private interface ProfileQuery {
        String[] PROJECTION = {
                ContactsContract.CommonDataKinds.Email.ADDRESS,
                ContactsContract.CommonDataKinds.Email.IS_PRIMARY,
        };

        int ADDRESS = 0;
        int IS_PRIMARY = 1;
    }

    /**
     * Represents an asynchronous login/registration task used to authenticate
     * the user.
     */
    public class UserLoginTask extends AsyncTask<Void, Void, Boolean> {

        private final String mEmail;
        private final String mPassword;

        UserLoginTask(String email, String password) {
            mEmail = email;
            mPassword = password;
        }

        @Override
        protected Boolean doInBackground(Void... params) {
            // TODO: attempt authentication against a network service.

            try {
                // Simulate network access.
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                return false;
            }

            for (String credential : DUMMY_CREDENTIALS) {
                String[] pieces = credential.split(":");
                if (pieces[0].equals(mEmail)) {
                    // Account exists, return true if the password matches.
                    return pieces[1].equals(mPassword);
                }
            }

            // TODO: register the new account here.
            return true;
        }

        @Override
        protected void onPostExecute(final Boolean success) {
            mAuthTask = null;
            showProgress(false);

            if (success) {
                finish();
            } else {
                toView.setError(getString(R.string.error_incorrect_password));
                toView.requestFocus();
            }
        }

        @Override
        protected void onCancelled() {
            mAuthTask = null;
            showProgress(false);
        }
    }
}


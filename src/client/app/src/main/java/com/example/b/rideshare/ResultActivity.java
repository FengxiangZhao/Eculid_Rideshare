package com.example.b.rideshare;

import android.app.Activity;
import android.app.ListActivity;
import android.database.Cursor;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.LoaderManager;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.SimpleCursorAdapter;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class ResultActivity extends Activity implements AdapterView.OnItemClickListener {
    private ListView listview;
    private List<String> dataList = null;



        @Override
        protected void onCreate (Bundle savedInstanceState){
            super.onCreate(savedInstanceState);
            setContentView(R.layout.content_result);
            dataList = new ArrayList<String>();
            for (int i = 0; i < 20; i++) {
                dataList.add(Integer.toString(i));
            }
            ListAdapter adapter = new ArrayAdapter<String>(ResultActivity.this,
                    android.R.layout.simple_list_item_1, dataList);
            listview = (ListView) findViewById(R.id.listview);
            listview.setAdapter(adapter);
            listview.setOnItemClickListener(this);
        }

        @Override
        public void onItemClick(AdapterView < ? > parent, View view,int position, long id){
            Toast.makeText(ResultActivity.this, "clicked " + position , Toast.LENGTH_SHORT).show();
        }


    }


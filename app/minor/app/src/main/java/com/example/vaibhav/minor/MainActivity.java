package com.example.vaibhav.minor;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import android.provider.DocumentsContract;
import android.speech.tts.TextToSpeech;
import android.app.Activity;
import android.content.Context;
import android.content.CursorLoader;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.BitmapFactory;
import android.hardware.Camera;
import android.hardware.Camera.CameraInfo;
import android.hardware.Camera.PictureCallback;
import android.media.CamcorderProfile;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnLongClickListener;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.Toast;

import android.media.MediaRecorder;

import static android.content.ContentValues.TAG;
import static android.provider.MediaStore.Files.FileColumns.MEDIA_TYPE_VIDEO;



////////////////////////////////////////

import android.app.ProgressDialog;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Base64;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.ImageRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;
import java.util.Locale;
import java.io.ByteArrayOutputStream;
import java.util.Map;

///////////////////////////////////////////////

public class MainActivity extends Activity {
    private Camera mCamera;
    private CameraPreview mPreview;
    private PictureCallback mPicture;
    private Button capture, switchCamera, postButton;
    private Context myContext;
    private LinearLayout cameraPreview;
    private boolean cameraFront = false;
    private boolean choice = false;

    ProgressDialog progressDialog;
    ProgressDialog progressDialog1;

    private MediaRecorder mediaRecorder;
    TextToSpeech t1,t2,t3,t4;
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        myContext = this;
        initialize();

        t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t1.setLanguage((new Locale("en", "IN")));
                }
            }
        }
        );
        t2=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t2.setLanguage((new Locale("en", "IN")));
                }
            }
        }
        );
        t3=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t3.setLanguage((new Locale("en", "IN")));
                }
            }
        }
        );
        t4=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t4.setLanguage((new Locale("en", "IN")));
                }
            }
        }
        );

        progressDialog = new ProgressDialog(this);
        progressDialog1 = new ProgressDialog(this);


    }


    private int findFrontFacingCamera() {
        int cameraId = -1;
        // Search for the front facing camera
        int numberOfCameras = Camera.getNumberOfCameras();
        for (int i = 0; i < numberOfCameras; i++) {
            CameraInfo info = new CameraInfo();
            Camera.getCameraInfo(i, info);
            if (info.facing == CameraInfo.CAMERA_FACING_FRONT) {
                cameraId = i;
                cameraFront = true;
                break;
            }
        }
        return cameraId;
    }

    private int findBackFacingCamera() {
        int cameraId = -1;
        //Search for the back facing camera
        //get the number of cameras
        int numberOfCameras = Camera.getNumberOfCameras();
        //for every camera check
        for (int i = 0; i < numberOfCameras; i++) {
            CameraInfo info = new CameraInfo();
            Camera.getCameraInfo(i, info);
            if (info.facing == CameraInfo.CAMERA_FACING_BACK) {
                cameraId = i;
                cameraFront = false;
                break;
            }
        }
        return cameraId;
    }

    public void onResume() {
        super.onResume();
        if (!hasCamera(myContext)) {
            Toast toast = Toast.makeText(myContext, "Sorry, your phone does not have a camera!", Toast.LENGTH_LONG);
            toast.show();
            finish();
        }
        if (mCamera == null) {
            //if the front facing camera does not exist
            if (findFrontFacingCamera() < 0) {
                Toast.makeText(this, "No front facing camera found.", Toast.LENGTH_LONG).show();
                switchCamera.setVisibility(View.GONE);
            }
            mCamera = Camera.open(findBackFacingCamera());
            mPicture = getPictureCallback();
            mPreview.refreshCamera(mCamera);
        }

    }

    public void initialize() {
        cameraPreview = (LinearLayout) findViewById(R.id.camera_preview);
        mPreview = new CameraPreview(myContext, mCamera);
        cameraPreview.addView(mPreview);

        capture = (Button) findViewById(R.id.button_capture);
        capture.setOnClickListener(videoListener);

        postButton = (Button) findViewById(R.id.button_send);
        postButton.setOnClickListener(sendListener);

        cameraPreview.setOnClickListener(captureListener);

        cameraPreview.setOnLongClickListener(captureListener2);

        switchCamera = (Button) findViewById(R.id.button_ChangeCamera);
        switchCamera.setOnClickListener(switchCameraListener);
        //switchCamera.setOnLongClickListener(switchCameraListener2);

    }

    OnClickListener switchCameraListener = new OnClickListener() {
        @Override
        public void onClick(View v) {
            //get the number of cameras
            int camerasNumber = Camera.getNumberOfCameras();
            if (camerasNumber > 1) {
                //release the old camera instance
                //switch camera, from the front and the back and vice versa
                choice = false;
                releaseCamera();
                chooseCamera();
            } else {
                Toast toast = Toast.makeText(myContext, "Sorry, your phone has only one camera!", Toast.LENGTH_LONG);
                toast.show();
            }
        }
    };

        public void chooseCamera() {
        //if the camera preview is the front

        if (cameraFront) {
            int cameraId = findBackFacingCamera();
            if (cameraId >= 0) {
                //open the backFacingCamera
                //set a picture callback
                //refresh the preview

                mCamera = Camera.open(cameraId);
                mPicture = getPictureCallback();
                mPreview.refreshCamera(mCamera);
            }
        } else {
            int cameraId = findFrontFacingCamera();
            if (cameraId >= 0) {
                //open the backFacingCamera
                //set a picture callback
                //refresh the preview

                mCamera = Camera.open(cameraId);
                mPicture = getPictureCallback();
                mPreview.refreshCamera(mCamera);
            }
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        //when on Pause, release camera in order to be used from other applications
        //releaseMediaRecorder();
        releaseCamera();
        super.onPause();
        if(t1 !=null){
            t1.stop();
            t1.shutdown();
        }
        // super.onPause();
        /*if(t2 !=null){
            t2.stop();
            t2.shutdown();
        }*/
         super.onPause();
        if(t3 !=null){
            t3.stop();
            t3.shutdown();
        }
        super.onPause();
        if(t4 !=null){
            t4.stop();
            t4.shutdown();
        }
        super.onPause();
    }

    private boolean hasCamera(Context context) {
        //check if the device has camera
        if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)) {
            return true;
        } else {
            return false;
        }
    }

    public void sendImage(byte[] data) {
        //TextToSpeech t1;

        try {
            RequestQueue requestQueue = Volley.newRequestQueue(getBaseContext());

            progressDialog.setMessage("Image upload in progress...");
            progressDialog.show();
            t1=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
                @Override
                public void onInit(int status) {
                    if(status != TextToSpeech.ERROR) {
                        t1.setLanguage((new Locale("en", "IN")));
                    }
                }
            }
            );
            //BitmapDrawable drawable = (BitmapDrawable) data;
            BitmapDrawable drawable = new BitmapDrawable(getResources(), BitmapFactory.decodeByteArray(data, 0, data.length));

            Bitmap bitmap = drawable.getBitmap();
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
            String encodedImage = Base64.encodeToString(byteArrayOutputStream.toByteArray(), Base64.DEFAULT);

            JSONObject jsonBody = new JSONObject();
            jsonBody.put("firstKey", "firstValue");
            jsonBody.put("ImageBLOB", encodedImage);

            String posturl = "http://192.168.43.180:5000/uploadimg";

            JsonObjectRequest jreq = new JsonObjectRequest(Request.Method.POST, posturl, jsonBody, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    String a = null;
                    try {
                        a = (String) response.get("name");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    progressDialog.dismiss();
                    Toast.makeText(MainActivity.this, a, Toast.LENGTH_SHORT).show();
                    //tts(a);
                    t1.speak(a, TextToSpeech.QUEUE_FLUSH, null);
                    //Toast.makeText(MainActivity.this, , Toast.LENGTH_SHORT).show();
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    progressDialog.dismiss();
                    Toast.makeText(MainActivity.this, "Failure", Toast.LENGTH_SHORT).show();
                }
            }) {
                @Override
                protected Map<String, String> getParams() throws AuthFailureError {
                    return super.getParams();
                }
            };
            jreq.setRetryPolicy(new DefaultRetryPolicy(
                    0,
                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

            //requestQueue.add(stringRequest);
            requestQueue.add(jreq);
        } catch (JSONException e) {
            Toast.makeText(MainActivity.this, "Json Error", Toast.LENGTH_SHORT).show();
        }
    }
    /*
    public void ttss(){
        t4=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
            @Override
            public void onInit(int status) {
                if(status != TextToSpeech.ERROR) {
                    t4.setLanguage((new Locale("en", "IN")));
                }
            }
        }
        );
    }*/
    public void sendHog(byte[] data) {
        //TextToSpeech t1;

        try {
            RequestQueue requestQueue = Volley.newRequestQueue(getBaseContext());

            progressDialog1.setMessage("Image upload in progress...");
            progressDialog1.show();
            t2=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
                @Override
                public void onInit(int status) {
                    if(status != TextToSpeech.ERROR) {
                        t2.setLanguage((new Locale("en", "IN")));
                    }
                }
            }
            );
            //BitmapDrawable drawable = (BitmapDrawable) data;
            BitmapDrawable drawable = new BitmapDrawable(getResources(), BitmapFactory.decodeByteArray(data, 0, data.length));

            Bitmap bitmap = drawable.getBitmap();
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, byteArrayOutputStream);
            String encodedImage = Base64.encodeToString(byteArrayOutputStream.toByteArray(), Base64.DEFAULT);

            JSONObject jsonBody = new JSONObject();
            jsonBody.put("firstKey", "firstValue");
            jsonBody.put("ImageHog", encodedImage);

            String posturl = "http://192.168.43.180:5000/uploadHog";

            JsonObjectRequest jreq = new JsonObjectRequest(Request.Method.POST, posturl, jsonBody, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    String aa = null;
                    try {
                        aa = (String) response.get("name");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    progressDialog1.dismiss();
                    Toast.makeText(MainActivity.this, aa, Toast.LENGTH_SHORT).show();
                    //tts(a);
                    t2.speak(aa, TextToSpeech.QUEUE_FLUSH, null);
                    //Toast.makeText(MainActivity.this, , Toast.LENGTH_SHORT).show();
                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    progressDialog1.dismiss();
                    Toast.makeText(MainActivity.this, "Failure", Toast.LENGTH_SHORT).show();
                }
            }) {
                @Override
                protected Map<String, String> getParams() throws AuthFailureError {
                    return super.getParams();
                }
            };
            jreq.setRetryPolicy(new DefaultRetryPolicy(
                    0,
                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

            //requestQueue.add(stringRequest);
            requestQueue.add(jreq);
        } catch (JSONException e) {
            Toast.makeText(MainActivity.this, "Json Error", Toast.LENGTH_SHORT).show();
        }
    }
    private PictureCallback getPictureCallback() {
        PictureCallback picture = new PictureCallback() {

            @Override
            public void onPictureTaken(byte[] data, Camera camera) {
                //make a new picture file
       //         ttss();
                File pictureFile = getOutputMediaFile();
                /*t4=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
                    @Override
                    public void onInit(int status) {
                        if(status != TextToSpeech.ERROR) {
                            t4.setLanguage((new Locale("en", "IN")));
                        }
                    }
                }
                );*/
                t4.speak("Detecting Person", TextToSpeech.QUEUE_FLUSH, null);
                if(choice == false) {
                    sendImage(data);
                }
                else if (choice == true) {
                    sendHog(data);
                }
                if (pictureFile == null) {
                    return;
                }
                try {
                    //write the file
                    FileOutputStream fos = new FileOutputStream(pictureFile);
                    fos.write(data);
                    fos.close();
                    Toast toast = Toast.makeText(myContext, "Picture saved: " + pictureFile.getName(), Toast.LENGTH_LONG);
                    toast.show();

                } catch (FileNotFoundException e) {
                } catch (IOException e) {
                }

                //refresh camera to continue preview
                mPreview.refreshCamera(mCamera);
            }
        };
        return picture;
    }

    OnClickListener captureListener = new OnClickListener() {
        @Override
        public void onClick(View v) {
            choice = false;
            mCamera.takePicture(null, null, mPicture);
        }
    };

    OnLongClickListener captureListener2 = new OnLongClickListener() {
        @Override
        public boolean onLongClick(View v) {
            choice = true;
            mCamera.takePicture(null, null, mPicture);
            return true;
        }

        //@Override
        public void onLngClick(View v) {
            mCamera.takePicture(null, null, mPicture);
        }
    };

    OnClickListener videoListener = new OnClickListener() {
        @Override
        public void onClick(View v) {


            Toast toast = Toast.makeText(myContext, "Capturing Video ", Toast.LENGTH_LONG);
            toast.show();
            //t2.speak("capturing video", TextToSpeech.QUEUE_FLUSH, null);
            Intent takeVideoIntent = new Intent(MediaStore.ACTION_VIDEO_CAPTURE);
            if (takeVideoIntent.resolveActivity(getPackageManager()) != null) {
                startActivityForResult(takeVideoIntent, 1);
            }


        }
    };
    public static final int PICK_VID = 1;
    OnClickListener sendListener = new OnClickListener() {
        @Override
        public void onClick(View v) {

            Toast toast = Toast.makeText(myContext, "Selecting Video ", Toast.LENGTH_LONG);
            toast.show();


            Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
            intent.setType("video/*");
            startActivityForResult(intent, PICK_PHOTO_FOR_AVATAR);


        }
    };


    private static final int PICK_PHOTO_FOR_AVATAR = 0;


    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == PICK_PHOTO_FOR_AVATAR && resultCode == Activity.RESULT_OK) {
            if (data == null) {
                //Display an error
                return;
            }
            //InputStream inputStream = getActivity().getContentResolver().openInputStream(data.getData());
            Uri selectedImageUri = data.getData();

            String wholeID = DocumentsContract.getDocumentId(selectedImageUri);

// Split at colon, use second item in the array
            String id = wholeID.split(":")[1];

            String[] column = { MediaStore.Video.Media.DATA };

// where id is equal to
            String sel = MediaStore.Video.Media._ID + "=?";

            Cursor cursor = getContentResolver().
                    query(MediaStore.Video.Media.EXTERNAL_CONTENT_URI,
                            column, sel, new String[]{ id }, null);

            String filePath = "";

            int columnIndex = cursor.getColumnIndex(column[0]);

            if (cursor.moveToFirst()) {
                filePath = cursor.getString(columnIndex);
            }

            cursor.close();



            //File tempFile = new File(Environment.getExternalStorageDirectory()+ "/my/part/my_0.mp4");
            File tempFile = new File(filePath);
            String encodedString = null;

            InputStream inputStream = null;
            try {
                inputStream = new FileInputStream(tempFile);
            } catch (Exception e) {
                // TODO: handle exception
            }
            byte[] bytes;
            byte[] buffer = new byte[8192];
            int bytesRead;
            ByteArrayOutputStream output = new ByteArrayOutputStream();
            try {
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    output.write(buffer, 0, bytesRead);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
            bytes = output.toByteArray();
            encodedString = Base64.encodeToString(bytes, Base64.DEFAULT);
            Log.i("String", encodedString);


            sendVid(encodedString);
            // MEDIA GALLERY
            //selectedImagePath = getPath(selectedImageUri);
            //Now you can do whatever you want with your inpustream, save it as file, upload to a server, decode a bitmap...
        }
    }


    public void sendVid(String data) {
        try {
            RequestQueue requestQueue = Volley.newRequestQueue(getBaseContext());
            final EditText edit = (EditText) findViewById(R.id.editText);
            String name = edit.getText().toString();
            progressDialog.setMessage("Video upload in progress...");
            progressDialog.show();
            t3=new TextToSpeech(getApplicationContext(), new TextToSpeech.OnInitListener() {
                @Override
                public void onInit(int status) {
                    //if(status != TextToSpeech.ERROR) {
                    //  t3.setLanguage((new Locale("en", "IN")));
                    //}
                }
            }
            );


            JSONObject jsonBody = new JSONObject();
            jsonBody.put("name", name);
            jsonBody.put("video", data);

            String posturl = "http://192.168.43.180:5000/uploadvid";
            t3.speak("Video Uploaded Successfully for training", TextToSpeech.QUEUE_FLUSH, null);

            JsonObjectRequest jreq = new JsonObjectRequest(Request.Method.POST, posturl, jsonBody, new Response.Listener<JSONObject>() {
                @Override
                public void onResponse(JSONObject response) {
                    progressDialog.dismiss();
                    Toast.makeText(MainActivity.this, "Video Uploaded for training", Toast.LENGTH_SHORT).show();
                    t3.speak("Video Uploaded Successfully for training", TextToSpeech.QUEUE_FLUSH, null);
                    String a = null;
                    try {
                        a = (String) response.get("name");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                    Toast.makeText(MainActivity.this, a, Toast.LENGTH_SHORT).show();

                }
            }, new Response.ErrorListener() {
                @Override
                public void onErrorResponse(VolleyError error) {
                    progressDialog.dismiss();
                    //Toast.makeText(MainActivity.this, "Failure", Toast.LENGTH_SHORT).show();
                    Toast.makeText(MainActivity.this, "Video Uploaded Successfully for training", Toast.LENGTH_SHORT).show();
                    t3.speak("Video Uploaded Successfully for training", TextToSpeech.QUEUE_FLUSH, null);
                }
            }) {
                @Override
                protected Map<String, String> getParams() throws AuthFailureError {
                    return super.getParams();
                }
            };
            jreq.setRetryPolicy(new DefaultRetryPolicy(
                    0,
                    DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                    DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));

            //requestQueue.add(stringRequest);
            requestQueue.add(jreq);
        } catch (JSONException e) {
            Toast.makeText(MainActivity.this, "Json Error", Toast.LENGTH_SHORT).show();
        }

    }

    //#######################################################################################

    //make picture and save to a folder
    private static File getOutputMediaFile() {
        //make a new file directory inside the "sdcard" folder
        File mediaStorageDir = new File("/sdcard/", "JCG Camera");

        //if this "JCGCamera folder does not exist
        if (!mediaStorageDir.exists()) {
            //if you cannot make this folder return
            if (!mediaStorageDir.mkdirs()) {
                return null;
            }
        }

        //take the current timeStamp
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        File mediaFile;
        //and make a media file:
        mediaFile = new File(mediaStorageDir.getPath() + File.separator + "IMG_" + timeStamp + ".jpg");

        return mediaFile;
    }

    private void releaseCamera() {
        // stop and release camera
        if (mCamera != null) {
            mCamera.release();
            mCamera = null;
        }
    }
}
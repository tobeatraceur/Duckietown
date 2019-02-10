package com.example.traceur.duckiebot;



import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.StrictMode;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import static com.example.traceur.duckiebot.R.*;

public class MainActivity extends Activity implements OnClickListener {

	private Button bnConnect,forward,back,left,right,stop,quit;
	private TextView txReceive;
	private EditText edIP, edPort, edData;

	private Handler handler = new Handler(Looper.getMainLooper());

	private TcpClient client = new TcpClient() {

		@Override
		public void onConnect(SocketTransceiver transceiver) {
			refreshUI(true);
		}

		@Override
		public void onDisconnect(SocketTransceiver transceiver) {
			refreshUI(false);
		}

		@Override
		public void onConnectFailed() {
			handler.post(new Runnable() {
				@Override
				public void run() {
					Toast.makeText(MainActivity.this, "连接失败",
							Toast.LENGTH_SHORT).show();
				}
			});
		}

		@Override
		public void onReceive(SocketTransceiver transceiver, final String s) {
			handler.post(new Runnable() {
				@Override
				public void run() {
					//txReceive.append(s);
				}
			});
		}
	};

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(layout.activity_main);

		StrictMode.setThreadPolicy(new StrictMode.ThreadPolicy.Builder()
				.detectDiskReads().detectDiskWrites().detectNetwork()
				.penaltyLog().build());
		//this.findViewById(R.id.bn_send).setOnClickListener(this);
		//bnConnect = (Button) this.findViewById(R.id.bn_connect);
		//bnConnect.setOnClickListener(this);
		forward = (Button) this.findViewById(id.button1);
		back = (Button) this.findViewById(id.button2);
		right = (Button) this.findViewById(id.button3);
		left = (Button) this.findViewById(id.button4);
		stop = (Button) this.findViewById(id.button5);
		quit = (Button) this.findViewById(id.button6);
		forward.setOnClickListener(this);
		back.setOnClickListener(this);
		right.setOnClickListener(this);
		left.setOnClickListener(this);
		stop.setOnClickListener(this);
		quit.setOnClickListener(this);
		edIP = (EditText) this.findViewById(id.ed_ip);
		edPort = (EditText) this.findViewById(id.ed_port);
		//edData = (EditText) this.findViewById(R.id.ed_dat);
		//txReceive = (TextView) this.findViewById(R.id.tx_receive);
		//txReceive.setOnClickListener(this);

		refreshUI(false);
	}

	@Override
	public void onStop() {
		client.disconnect();
		super.onStop();
	}

	@Override
	public void onClick(View v) {
		switch (v.getId()) {
//		case R.id.bn_connect:
//			connect();
//			break;
//		case R.id.bn_send:
//			sendStr();
//			break;
//		case R.id.tx_receive:
//			clear();
//			break;
        case id.button1:
            connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
            if(client.isConnected())
            	sendStr("w");
            break;
		case id.button2:
			connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
			if(client.isConnected())
				sendStr("s");
			break;
		case id.button3:
			connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
			if(client.isConnected())
				sendStr("d");
			break;
		case id.button4:
			connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
			if(client.isConnected())
				sendStr("a");
			break;
		case id.button5:
			connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
			if(client.isConnected())
				sendStr(" ");
			break;
		case id.button6:
			connect();
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				return;
			}
			if(client.isConnected())
				sendStr("q");
			break;
		}
	}

	/**
	 * 刷新界面显示
	 * 
	 * @param isConnected
	 */
	private void refreshUI(final boolean isConnected) {
		handler.post(new Runnable() {
			@Override
			public void run() {
				edPort.setEnabled(!isConnected);
				edIP.setEnabled(!isConnected);
				//bnConnect.setText(isConnected ? "断开" : "连接");
			}
		});
	}

	/**
	 * 设置IP和端口地址,连接或断开
	 */
	private void connect() {
		if (client.isConnected()) {
			// 断开连接
			client.disconnect();
		} else {
			try {
				String hostIP = edIP.getText().toString();
				int port = Integer.parseInt(edPort.getText().toString());
				client.connect(hostIP, port);
			} catch (NumberFormatException e) {
				Toast.makeText(this, "端口错误", Toast.LENGTH_SHORT).show();
				e.printStackTrace();
			}
		}
	}

	/**
	 * 发送数据
	 */
	private void sendStr(String data) {
		try {
			//String data = edData.getText().toString();
			client.getTransceiver().send(data);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	/**
	 * 清空接收框
	 */
	private void clear() {
		new AlertDialog.Builder(this).setTitle("确认清除?")
				.setNegativeButton("取消", null)
				.setPositiveButton("确认", new DialogInterface.OnClickListener() {
					@Override
					public void onClick(DialogInterface dialog, int which) {
						//txReceive.setText("");
					}
				}).show();
	}
}

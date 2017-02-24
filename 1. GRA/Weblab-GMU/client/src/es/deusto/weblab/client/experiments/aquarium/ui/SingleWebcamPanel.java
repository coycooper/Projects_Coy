/*
* Copyright (C) 2012 onwards University of Deusto
* All rights reserved.
*
* This software is licensed as described in the file COPYING, which
* you should have received as part of this distribution.
*
* This software consists of contributions made by many individuals, 
* listed below:
*
* Author: Pablo Orduña <pablo.orduna@deusto.es>
*
*/

package es.deusto.weblab.client.experiments.aquarium.ui;

import com.google.gwt.core.client.GWT;
import com.google.gwt.json.client.JSONObject;
import com.google.gwt.json.client.JSONParser;
import com.google.gwt.json.client.JSONValue;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import es.deusto.weblab.client.configuration.IConfigurationRetriever;
import es.deusto.weblab.client.lab.experiments.IDisposableWidgetsContainer;
import es.deusto.weblab.client.ui.widgets.IWlDisposableWidget;
import es.deusto.weblab.client.ui.widgets.WlWebcam;

public class SingleWebcamPanel extends Composite implements IDisposableWidgetsContainer {

	private static SingleWebcamPanelUiBinder uiBinder = GWT.create(SingleWebcamPanelUiBinder.class);

	@UiField(provided=true) WlWebcam webcam;
	
	private IConfigurationRetriever configurationRetriever;
	
	interface SingleWebcamPanelUiBinder extends UiBinder<Widget, SingleWebcamPanel> {
	}
	
	public SingleWebcamPanel(IConfigurationRetriever configurationRetriever, String initialConfiguration, int camera) {
		
		this.configurationRetriever = configurationRetriever;
		
		this.webcam = GWT.create(WlWebcam.class);
		this.webcam.setTime(this.configurationRetriever);
		initWidget(uiBinder.createAndBindUi(this));
		
		parseWebcamConfig(initialConfiguration, camera);
	}
	
	public void start() {
		this.webcam.start();
	}
	
	private void parseWebcamConfig(String initialConfiguration, int camera) {
		System.out.println("Aquarium: initial config:" + initialConfiguration);
		final JSONValue initialConfigValue   = JSONParser.parseStrict(initialConfiguration);
	    final JSONObject initialConfigObject = initialConfigValue.isObject();
	    if(initialConfigObject == null) {
	    	Window.alert("Error parsing aquarium configuration: not an object: " + initialConfiguration);
	    	return;
	    }
	    
	    configureWebcam(this.webcam, initialConfigObject, camera);
	}
	
	private void configureWebcam(WlWebcam webcam, JSONObject initialConfigObject, int number) {
		final JSONValue webcamValue = initialConfigObject.get("webcam" + number);
	    if(webcamValue != null) {
	    	final String urlWebcam = webcamValue.isString().stringValue();
	    	webcam.setUrl(urlWebcam);
	    }
	    
	    final JSONValue mjpegValue = initialConfigObject.get("mjpeg" + number);
	    if(mjpegValue != null) {
	    	final String mjpeg = mjpegValue.isString().stringValue();
	    	int width = 320;
	    	int height = 240;
	    	if(initialConfigObject.get("mjpegWidth" + number) != null) {
	    		final JSONValue mjpegWidth = initialConfigObject.get("mjpegWidth" + number);
	    		if(mjpegWidth.isNumber() != null) {
	    			width = (int)mjpegWidth.isNumber().doubleValue();
	    		} else if(mjpegWidth.isString() != null) {
	    			width = Integer.parseInt(mjpegWidth.isString().stringValue());
	    		}
	    	}
	    	if(initialConfigObject.get("mjpegHeight" + number) != null) {
	    		final JSONValue mjpegHeight = initialConfigObject.get("mjpegHeight" + number);
	    		if(mjpegHeight.isNumber() != null) {
	    			height = (int)mjpegHeight.isNumber().doubleValue();
	    		} else if(mjpegHeight.isString() != null) {
	    			height = Integer.parseInt(mjpegHeight.isString().stringValue());
	    		}
	    	}
	    	webcam.setStreamingUrl(mjpeg, width, height);
	    }
	}


	@Override
	public IWlDisposableWidget[] getDisposableWidgets() {
		return new IWlDisposableWidget[]{ this.webcam };
	}


	@Override
	public Widget asGwtWidget() {
		return this;
	}
}

# *****************************************************************************
# Copyright (c) 2016 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#   Lokesh Haralakatta  - Initial Contribution
# *****************************************************************************

import ibmiotf.device
import ibmiotf.application
import uuid
import os
from ibmiotf import *
from nose.tools import *
from nose import SkipTest
import logging
import testUtils

class TestDevice(testUtils.AbstractTest):
    registeredDevice = None
    deviceClient = None
    managedClient = None

    DEVICE_TYPE = "test_device"
    DEVICE_ID = str(uuid.uuid4())
    
    @classmethod
    def setup_class(self):
        try: 
            deviceType = self.setupAppClient.api.getDeviceType(self.DEVICE_TYPE)
        except APIException as e:
            if e.httpCode == 404:
                deviceType = self.setupAppClient.api.addDeviceType(self.DEVICE_TYPE)
            else: 
                raise e
        
        self.registeredDevice = self.setupAppClient.api.registerDevice(self.DEVICE_TYPE, self.DEVICE_ID)
        
        self.options={
            "org": self.ORG_ID,
            "type": self.registeredDevice["typeId"],
            "id": self.registeredDevice["deviceId"],
            "auth-method": "token",
            "auth-token": self.registeredDevice["authToken"]
        }
        
        self.deviceClient = ibmiotf.device.Client(self.options)

        #Create default DeviceInfo Instance and associate with ManagedClient Instance
        deviceInfoObj = ibmiotf.device.DeviceInfo()
        deviceInfoObj.fwVersion = 0.0
        self.managedClient = ibmiotf.device.ManagedClient(self.options, deviceInfo=deviceInfoObj)    

    @classmethod
    def teardown_class(self):
        del self.deviceClient
        del self.managedClient
        self.setupAppClient.api.deleteDevice(self.DEVICE_TYPE, self.DEVICE_ID)
    
    
    @raises(Exception)
    def testMissingOptions(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({})
        assert_equal(e.exception.msg, 'Missing required property: org')

    @raises(Exception)
    def testMissingOrg(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({"org": None, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                   "auth-method": "token", "auth-token": self.registeredDevice["authToken"] })
        assert_equal(e.exception.msg, 'Missing required property: org')

    @raises(Exception)
    def testMissingType(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({"org": self.ORG_ID, "type": None, "id": self.registeredDevice["deviceId"],
                                   "auth-method": "token", "auth-token": self.registeredDevice["authToken"] })
        assert_equal(e.exception.msg, 'Missing required property: type')

    @raises(Exception)
    def testMissingId(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": None,
                                   "auth-method": "token", "auth-token": self.registeredDevice["authToken"]})
        assert_equal(e.exception.msg, 'Missing required property: id')

    @raises(Exception)
    def testMissingAuthMethod(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                   "auth-method": None, "auth-token": self.registeredDevice["authToken"]})
        assert_equal(e.exception.msg, 'Missing required property: auth-method')

    @raises(Exception)
    def testMissingAuthToken(self):
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                   "auth-method": "token", "auth-token": None })
        assert_equal(e.exception.msg, 'Missing required property: auth-token')

    @raises(Exception)
    def testUnSupportedAuthMethod(self):
        with assert_raises(UnsupportedAuthenticationMethod) as e:
            ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                   "auth-method": "unsupported-method", "auth-token": self.registeredDevice["authToken"]})
        assert_equal(e.exception_type,UnsupportedAuthenticationMethod)

    def testDeviceClientInstance(self):
        deviceCli = ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                           "auth-method": "token", "auth-token": self.registeredDevice["authToken"]})
        assert_is_instance(deviceCli , ibmiotf.device.Client)

    @raises(Exception)
    def testMissingConfigFile(self):
        deviceFile="InvalidFile.out"
        with assert_raises(ConfigurationException) as e:
            ibmiotf.device.ParseConfigFile(deviceFile)
        assert_equal(e.exception.msg, 'Error reading device configuration file')

    @raises(Exception)
    def testInvalidConfigFile(self):
        deviceFile="nullValues.conf"
        with assert_raises(AttributeError) as e:
            ibmiotf.device.ParseConfigFile(deviceFile)
        assert_equal(e.exception, AttributeError)
    
    @SkipTest
    def testNotAuthorizedConnect(self):
        client = ibmiotf.device.Client({"org": self.ORG_ID, "type": self.registeredDevice["typeId"], "id": self.registeredDevice["deviceId"],
                                              "auth-method": "token", "auth-token": "MGhUixxxxxxxxxxxx", "auth-key":"a-xxxxxx-s1tsofmoxo"})
        with assert_raises(ConnectionException) as e:
            client.connect()
        assert_equals(e.exception, ConnectionException)
        assert_equals(e.exception.msg,'Not authorized')

    @SkipTest
    def testMissingMessageEncoder(self):
        with assert_raises(MissingMessageEncoderException)as e:
            myData={'name' : 'foo', 'cpu' : 60, 'mem' : 50}
            self.deviceClient.connect()
            self.deviceClient.publishEvent("missingMsgEncode", "jason", myData)
        assert_equals(e.exception, MissingMessageEncoderException)
    
    def testDeviceInfoInstance(self):
        deviceInfoObj = ibmiotf.device.DeviceInfo()
        assert_is_instance(deviceInfoObj, ibmiotf.device.DeviceInfo)
        print(deviceInfoObj)

    def testDeviceFirmwareInstance(self):
        deviceFWObj = ibmiotf.device.DeviceFirmware()
        assert_is_instance(deviceFWObj, ibmiotf.device.DeviceFirmware)
        print(deviceFWObj)

    def testManagedClientInstance(self):
        managedClient = ibmiotf.device.ManagedClient(self.options)
        assert_is_instance(managedClient, ibmiotf.device.ManagedClient)

    def testKeepAliveIntervalMethods(self):
        assert_equals(self.deviceClient.getKeepAliveInterval(), 60)
        self.deviceClient.setKeepAliveInterval(120)
        self.deviceClient.connect()
        assert_equals(self.deviceClient.getKeepAliveInterval(), 120)
        self.deviceClient.disconnect()
        
    def testPublishEvent(self):
        def devPublishCallback():
            print("Device Publish Event done!!!")

        myData={'name' : 'foo', 'cpu' : 60, 'mem' : 50}
        self.deviceClient.connect()
        assert_true(self.deviceClient.publishEvent("testPublishJsonEvent", "json", myData,on_publish=devPublishCallback,qos=2))
        assert_true(self.deviceClient.publishEvent("testPublishXMLEvent", "xml", myData,on_publish=devPublishCallback,qos=2))
        self.deviceClient.disconnect()
    
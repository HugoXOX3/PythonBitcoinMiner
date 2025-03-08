===============================
How to Build an iOS Mining App
===============================

This guide will walk you through the steps to build an iOS mining app using SwiftUI and Python. The app allows users to configure mining settings and execute a mining script.

Prerequisites
=============

- Xcode installed on your macOS system. 

Setting Up the Project
======================

1. **Open Xcode** and create a new project:
   - Choose "App" under the iOS tab and click "Next."
   - Enter the project name, organization name, and identifier.
   - Choose the interface and lifecycle as "SwiftUI" and "SwiftUI App" respectively.
   - Click "Next" and choose a location to save the project.

Adding Pyto Dependency
======================

To run Python scripts within the iOS app, we will use the Pyto library.

1. **Using CocoaPods**:
   - Create a `Podfile` in your project directory with the following content:

     .. code-block:: ruby

        platform :ios, '14.0'
        use_frameworks!

        target 'YourProjectName' do
          pod 'Pyto'
        end

   - Run `pod install` in the terminal to install the dependency.
   - Open the generated `.xcworkspace` file to continue working on your project.

Download the dir of iosbitcoinminer
==============================

Download the [iosbitcoinminer](https://github.com/HugoXOX3/PythonBitcoinMiner/tree/main/iosbitcoinminer)

Building and Running the App
============================

1. **Connect your iOS device** or use a simulator.
2. Click the "Run" button in Xcode to build and run the app.

With these steps, you have successfully built an iOS mining app that allows users to configure mining settings and execute a mining script.

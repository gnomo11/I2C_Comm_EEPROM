# I2C_Comm_EEPROM

Project made for reading and writing on an EEPROM memory through I2C communication through the PIC18F45K50 microcontroller and a GUI  developed in Python
![i2c_eeprom_gui](https://user-images.githubusercontent.com/91303136/231664657-6685d7d9-f600-4dee-9c7f-2120ec0b984b.jpg)

By clicking on the memory icon, the microcontroller connects to the interface, if the operation was successful, the icon is painted green:
![init_comm_with_pic](https://user-images.githubusercontent.com/91303136/231665353-b3f5cc53-864f-4c17-850c-a500a5e3aab9.jpg)

To start the writing process click on the Data icon\n:
![start_writting](https://user-images.githubusercontent.com/91303136/231665803-ee1a1a4c-fc96-4e82-b210-20f2025bb3f8.jpg)

Set the data value and the data address. Then click on the button "Write Data" and wait until the progress bar is completed:
![data_saved](https://user-images.githubusercontent.com/91303136/231666102-92a73ebd-33fe-4ebc-a572-f9a0983904c9.jpg)

To read the stored data just set the data address to be read:
![Set_data_address_to_read](https://user-images.githubusercontent.com/91303136/231666578-a3d3e109-1b14-467d-bfe5-f3b4b825dcfc.jpg)

The data should be displayed:
![Data_reading](https://user-images.githubusercontent.com/91303136/231666792-696fb4cd-4b41-4d9c-9ec8-cfde660e7be9.jpg)

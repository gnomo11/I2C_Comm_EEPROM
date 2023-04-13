/*	MEMORIA I2C */

#include <18F45K50.h>
#fuses NOWDT
#use delay(internal=48MHz)
#use i2c(master, scl=PIN_B1, sda=PIN_B0, fast=300000, FORCE_HW)

//-----------------------------------------------------------------------
#include <stdlib.h>
#include <usb_cdc.h>
#include <string.h>
//-----------------------------------------------------------------------
#define LED PIN_A0
//---------------------------------------------------------------------------
//char mens[50],address[4],rdi[5],tecla=0,opd[5];
char dat[6], dir[4];
int i=0,j=0;
short have_data = 0, have_data2 = 0;
short check = 0;
long direction = 0, data = 0;
int a=0, returned = 0;
//---------------------------------------------------------------------------

void receive_data(void);
void EEPROM_SAVE(long direc_write, int dat);
int EEPROM_READ (long direc_read);


void main(void) {
	
	usb_cdc_init(); //configurar puerto virtual
	usb_init(); //inicializamos el stack USB
	while(!usb_cdc_connected()); //esperar a detectar comunicación

	output_drive(LED);
	output_low(LED);


	while(true){
		
		usb_task(); //ejecutar cada tanto tiempo para que el PC no nos deje de atender


		receive_data();		


		if (a==1){
			if(data<256 && direction < 4096 ){EEPROM_SAVE(direction,data);}
		}
	
		else if (a == 2){
			if(direction < 4096 && check == 0){returned = EEPROM_READ(direction); printf(usb_cdc_putc,"%u\n",returned);check = 1;}
		}

		delay_ms(100);
	}
}

//---------------------------------------------------------------------------

void receive_data (void){

	if(usb_cdc_kbhit()){ //verifica si hay un caracter...
			
			//D/E XXXX F
			while(have_data == 0){ 
				dat[i]=usb_cdc_getc();
				if(dat[i] == 'F'){have_data = 1;}
				i++;
			}


			if(dat[0] == 'O'){
			
				while(have_data2 == 0){
					dir[j] = dat[j+1];
					if(dir[j]=='F'){have_data2=1;}
					j++;
				}

				if(have_data2==1){
                  a=atoi(dir);have_data2=0;check=0;
				  //printf(usb_cdc_putc,"%u",a);
                  }
				
			}

			if(dat[0] == 'D'){
			
				while(have_data2 == 0){
					dir[j] = dat[j+1];
					if(dir[j]=='F'){have_data2=1;}
					j++;
				}

				if(have_data2==1){
                  direction=atol(dir);have_data2=0;
				  //printf(usb_cdc_putc,"%lu",direction);
                  }
				
			}
				
			
			if(dat[0] == 'E'){

				while(have_data2 == 0){
					dir[j] = dat[j+1];
					if(dir[j]=='F'){have_data2=1;}
					j++;
				}

				if(have_data2==1){
                  data=atol(dir);have_data2=0;
				  //printf(usb_cdc_putc,"%lu",data);
                  }
			}

			have_data=0;i=0;j=0;
			
		}


}

//-----------------------------------------------------

void EEPROM_SAVE(long direc_write, int dat){
   i2c_start();
   i2c_write(0xAE);
   i2c_write(direc_write >> 8); //enviar la parte ALTA
   i2c_write(direc_write); //enviar la parte BAJA
   i2c_write(dat);
   i2c_stop();
   delay_us(10);
}

//-------------------------------------------------------------

int EEPROM_READ (long direc_read){
   int data_return;

   i2c_start();
   i2c_write (0xAE); 
   i2c_write(direc_read >> 8);
   i2c_write(direc_read);
   i2c_start();
   i2c_write(0xAF);
   data_return=i2c_read(0);
   i2c_stop();
   delay_us(10);
   return (data_return);
}

//-------------------------------------------------------------

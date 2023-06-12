import numpy as np
import cv2 as cv
import logging
from PyQt5.QtWidgets import QFileDialog, QMessageBox
logging.basicConfig(level=logging.DEBUG,filename="Logging.log",format='%(lineno)s - %(levelname)s - %(message)s',filemode='w')
logger = logging.getLogger()
class modes() :

    def __init__(self):
        pass
    def __init__(self, path):
        # Read image from path as a grayscale image
        self.img = cv.imread(path,0)

        # Compute the 2-dimensional discrete Fourier Transform of the image
        self.f = np.fft.fft2(self.img)

        # Shift zero frequency component to the center of the spectrum
        self.fShift=np.fft.fftshift(self.f)

        # Compute the magnitude spectrum of the shifted Fourier Transform 
        self.mag = 20 * np.log(np.abs(self.fShift))

        # Compute the phase spectrum of the shifted Fourier Transform 
        self.phase = np.angle(self.fShift)

        # Compute the real part of the shifted Fourier Transform 
        self.real = 20 * np.log(np.real(self.fShift))

        # Compute the imaginary part of the shifted Fourier Transform 
        self.imaginary = 20 * np.log(np.imag(self.fShift))

        # Set all negative values in the imaginary part of the shifted Fourier Transform to a small positive value
        # This line sets all the negative or zero values in the self.imaginary array to a small positive value 10 ** -8. 
        # It ensures that the imaginary spectrum does not contain negative values, which could cause problems when processing the image.
        self.imaginary[self.imaginary <= 0] = 10 ** -9

        # Compute the real part of the original Fourier Transform 
        self.reall = np.real(self.f)

        # Compute the imaginary part of the original Fourier Transform 
        self.imaginaryy = np.imag(self.f)

        # Compute the magnitude spectrum of the original Fourier Transform 
        self.magnitudee = np.abs(self.f)

        # Compute the phase spectrum of the original Fourier Transform 
        self.phasee = np.angle(self.f)

        # Store the shape of the image as a tuple
        self.imgshape = self.img.shape

        # Create a matrix with the same shape as the image and fill it with ones
        self.uniformMagnitude = np.ones(self.img.shape)

        # Create a matrix with the same shape as the image and fill it with zeros
        self.uniformPhase = np.ones(self.img.shape)
        # self.uniformPhase = np.zeros(self.img.shape)


    def mix(self, imageToBeMixed: 'modes', magnitudeRealoruniformmagRatio: float, phaseimageoruniformphaseRatio: float, comp1 , comp2 ):

        w1 = magnitudeRealoruniformmagRatio
        w2 = phaseimageoruniformphaseRatio

        # Set the attribute 'first' to comp1
        self.first = comp1

        # Set the attribute 'second' to comp2
        self.second = comp2

        # Initialize a variable called mixInverse to None
        mixInverse = None

        # 1. Calculates the weighted sum of the magnitudes of the image and the self object. The weight is defined by the variable 'w1'
        # 2. Calculates the weighted sum of the phases of the image and the self object. The weight is defined by the variable 'w2'
        # 3. Multiplies the results of steps 1 and 2 together
        # 4. Takes the inverse Fourier transform of the result of step 3
        # 5. Takes the real part of the result of step 4
        # The resulting image is a mix of the magnitudes of the input image and the self object, weighted by 'w1', and a mix of the phases of the input image and the self object, weighted by 'w2'.
        if (self.first == 'magnitude' and self.second == 'phase') or (self.first == 'phase' and self.second == 'magnitude'):
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.magnitudee) + w1 * (self.magnitudee)), np.exp(1j * (w2 * (imageToBeMixed.phasee) + (1 - w2) * (self.phasee))))))
        
        # multiply the magnitude and uniform phase images by their respective weights and 
        # add the complement of the weights multiplied by the other image's magnitude or uniform phase
        elif (self.first == 'magnitude' and self.second == 'uniform phase') or (self.first == 'uniform phase' and self.second == 'magnitude'):
            # take the inverse Fourier transform of the mixed image and extract the real part
            # mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.magnitudee) + w1 * (self.magnitudee)), np.exp(1j * (w2 * (imageToBeMixed.uniformPhase) + (1 - w2) * (self.uniformPhase))))))
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.magnitudee) + w1 * (self.magnitudee)), np.exp(1j * (w2 *0.2* (imageToBeMixed.phase) + (1 - w2) * (self.uniformPhase))))))
        
        # Check if the first property is 'phase' and the second is 'uniform magnitude' or if the first is 'uniform magnitude' and the second is 'phase'
        elif (self.first == 'phase' and self.second == 'uniform magnitude') or (self.first == 'uniform magnitude' and self.second == 'phase'):
            # Compute the mixed inverse by multiplying the weighted sum of the uniform magnitudes with the complex exponential of the weighted sum of the phases, then taking the real part of the inverse Fourier transform of the result
            mixInverse1 = np.real(np.fft.ifft2(np.multiply(((1 - w1) * (imageToBeMixed.uniformMagnitude) + w1 * (self.uniformMagnitude)), np.exp(1j * (w2 * (imageToBeMixed.phasee) + (1 - w2) * (self.phasee))))))
        
        # Check if the mixing types are 'real' and 'imaginary' or 'imaginary' and 'real'
        elif (self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
            # Mix the real and imaginary components of the images using the weights w1 and w2
            mixInverse = np.real(np.fft.ifft2((w1*(self.reall) + (1-w1)*(imageToBeMixed.reall)) + ((1-w2)*(self.imaginaryy) + w2*(imageToBeMixed.imaginaryy)) * 1j))
        
        if(self.first == 'real' and self.second =='imaginary') or (self.first == 'imaginary' and self.second =='real'):
            return abs(mixInverse)
        else:
            return abs(mixInverse1)
        

    def drawmix(self):
        data = ...
        #retrieve the values from two sliders 
        firstvalue = self.gains[0].value() / 100
        secondvalue = self.gains[1].value() / 100

        #mixing modes buttons
        self.comp1=self.comboboxes[2].currentText()
        self.comp2=self.comboboxes[3].currentText()

        if (self.comboboxes[2].currentText() == 'magnitude' and self.comboboxes[3].currentText() == 'phase') or(self.comboboxes[2].currentText() == 'real' and self.comboboxes[3].currentText() == 'imaginary') or (self.comboboxes[2].currentText() == 'magnitude' and self.comboboxes[3].currentText() == 'uniform phase') or (self.comboboxes[2].currentText() == 'uniform magnitude' and self.comboboxes[3].currentText() == 'phase') or (self.comboboxes[2].currentText() == 'uniform magnitude' and self.comboboxes[3].currentText() == 'uniform phase'):
            data = self.source1.mix(self.source2, firstvalue, secondvalue, self.comp1 , self.comp2 )
        elif (self.comboboxes[2].currentText() == 'phase' and self.comboboxes[3].currentText() == 'magnitude') or (self.comboboxes[2].currentText() == 'imaginary' and self.comboboxes[3].currentText() == 'real') or (self.comboboxes[2].currentText() == 'uniform phase' and self.comboboxes[3].currentText() == 'magnitude') or (self.comboboxes[2].currentText() == 'phase' and self.comboboxes[3].currentText() == 'uniform magnitude') or (self.comboboxes[2].currentText() == 'uniform phase' and self.comboboxes[3].currentText() == 'uniform magnitude'):
            data = self.source2.mix(self.source1, secondvalue, firstvalue, self.comp1 , self.comp2 )
        self.mixplace.show()
        self.mixplace.setImage(data.T)
        if type(data) != type(...):
            logger.info(f"Mixing {firstvalue} {self.comboboxes[2].currentText()} From {self.comboboxes[5].currentText() } And {secondvalue}"
                f" {self.comboboxes[3].currentText()} From {self.comboboxes[6].currentText()}")
            logger.info(f"{self.comboboxes[4].currentText()} has been generated and displayed")

    def components(self, imageOriginalNum, imageBoxNum, imgno, mode):
        # Show the plot for the current image box
        self.plot[imageBoxNum].show()
    
        # Set the image for the current image box based on the selected mode
        if mode == self.component[1]:
            self.plot[imageBoxNum].setImage((self.images[imageOriginalNum].mag.T))
        elif mode == self.component[2]:
            self.plot[imageBoxNum].setImage(self.images[imageOriginalNum].phase.T)
        elif mode == self.component[3]:
            self.plot[imageBoxNum].setImage((self.images[imageOriginalNum].real.T))
        elif mode == self.component[4]:
            self.plot[imageBoxNum].setImage(self.images[imageOriginalNum].imaginary.T)
    
        # Log a message indicating which mode was plotted for which image
        logger.info(f"plot {mode} of image {imgno}")
    

    def outputplace(self):
        if self.comboboxes[4].currentText() == 'Slot 1' :
            self.mixplace = self.plot[4]
        elif self.comboboxes[4].currentText() == 'Slot 2' :
            self.mixplace = self.plot[5]

    def othercomponent(self ,mode1 ,mode2 ):
        self.comboboxes[mode2].clear()
        for Mixer_option in range(len(self.Mixer_options)):
            if self.comboboxes[mode1].currentText().lower() in self.Mixer_options[Mixer_option]:
                if Mixer_option % 2 == 0:
                    Mixer_option = Mixer_option + 1
                else:
                    Mixer_option = Mixer_option - 1
                self.comboboxes[mode2].addItems(self.Mixer_options[Mixer_option])

    def source(self):
        if self.comboboxes[5].currentText() == 'image 1' :
            self.source1 = self.img1
        elif self.comboboxes[5].currentText() == 'image 2' :
            self.source1 = self.img2
        if self.comboboxes[6].currentText() == 'image 1' :
            self.source2 = self.img1
        elif self.comboboxes[6].currentText() == 'image 2' :
            self.source2 = self.img2
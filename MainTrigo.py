import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from trigo import Ui_MainWindow
import math

class Main():
    def __init__(self):
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.clear.clicked.connect(self.clearLineEdit)
        self.ui.striangle.clicked.connect(self.showTriangle)
        self.ui.Clear_list.clicked.connect(self.clearListWidget)
        self.ui.calculer.clicked.connect(self.negatifCheck)


    def clearLineEdit(self):
        self.ui.AB.setText("")
        self.ui.AC.setText("")
        self.ui.BC.setText("")
        self.ui.alpha.setText("")
        self.ui.beta.setText("")
        self.ui.alpha_rad.setText("")
        self.ui.beta_rad.setText("")

    def showTriangle(self):
        if self.ui.AC.text() == "" or self.ui.BC.text() == "":
            return self.ui.listWidget.addItem("AC and/or BC no value")
        AC=float(self.ui.AC.text())
        BC=float(self.ui.BC.text())

        self.widget = QMainWindow()
        self.widget.setWindowTitle("Triangle view")

        self.textLabel = QLabel(self.widget)
        self.textLabel.setPixmap(QPixmap("TrigoTriangle.png"))
        self.textLabel.setScaledContents(True)

        a=500
        if AC >= BC:
            b=int(a*BC/AC)
            self.widget.setGeometry(50,50,int(a+20),int(b+20))
            self.textLabel.setGeometry(10,10,a,b)
        else:
            b=int(a*AC/BC)
            self.widget.setGeometry(50,50,int(b+20),int(a+20))
            self.textLabel.setGeometry(10,10,b,a)
        
        self.widget.show()

    def clearListWidget(self):
        self.ui.listWidget.clear()

    # warne negative value entered before calcule decision    
    def negatifCheck(self):

        # set void LineEdit to 0
        if self.ui.AB.text() == "":
            self.ui.AB.setText("0")
        if self.ui.AC.text() == "":
            self.ui.AC.setText("0")
        if self.ui.BC.text() == "":
            self.ui.BC.setText("0")
        if self.ui.alpha.text() == "":
            self.ui.alpha.setText("0")
        if self.ui.beta.text() == "":
            self.ui.beta.setText("0")
        if self.ui.alpha_rad.text() == "":
            self.ui.alpha_rad.setText("0")
        if self.ui.beta_rad.text() == "":
            self.ui.beta_rad.setText("0")

        #import all LineEdit
        AB=float(self.ui.AB.text())
        AC=float(self.ui.AC.text())
        BC=float(self.ui.BC.text())
        alpha=float(self.ui.alpha.text())
        beta=float(self.ui.beta.text())
        alpharad=float(self.ui.alpha_rad.text())
        betarad=float(self.ui.beta_rad.text())

        # popup window "show detail text" container
        detailText=""
        
        if AB < 0 :
            detailText += "AB={} ".format(AB)
        if AC < 0 :
            detailText += "AC={} ".format(AC)
        if BC < 0 :
            detailText += "BC={} ".format(BC)
        if alpha < 0 :
            detailText += "alpha={} ".format(alpha)
        if beta < 0 :
            detailText += "beta={} ".format(beta)
        if alpharad < 0 :
            detailText += "alpharad={} ".format(alpharad)
        if betarad < 0:
            detailText += "batarad={} ".format(betarad)

        if detailText != "":
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("WARNING : negative value entered")
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setDetailedText(detailText)
            x = msg.exec_()
            self.CalculChoice()
        else:
            self.CalculChoice()

    # calcul decision
    def CalculChoice(self):
        self.ui.listWidget.addItem("____________________________________________________________________________________")

        # import all LineEdit
        AB=float(self.ui.AB.text())
        AC=float(self.ui.AC.text())
        BC=float(self.ui.BC.text())
        alpha=float(self.ui.alpha.text())
        beta=float(self.ui.beta.text())
        alpharad=float(self.ui.alpha_rad.text())
        betarad=float(self.ui.beta_rad.text())
        cs=int(self.ui.ChiffreSign.text())
        self.ui.listWidget.addItem("entered AB={} / AC={} / BC={} / alpha={} / beta={} / alpharad={} / betarad={}".format(AB,AC,BC,alpha,beta,alpharad,betarad))

        # check cohérence °/rad
        if alpha != 0 and alpharad != 0 and abs(self.Arrondi(alpharad,cs)-self.Arrondi(alpha*math.pi/180,cs)) >= 1/10**cs:
            self.clear0()
            return self.ui.listWidget.addItem("alpha °/rad error : alpharad={} alpha en rad={}".format(self.Arrondi(alpharad,cs),self.Arrondi(alpha*math.pi/180,cs)))
        if beta != 0 and betarad != 0 and abs(self.Arrondi(betarad,cs)-self.Arrondi(beta*math.pi/180,cs)) >= 1/10**cs:
            self.clear0()
            return self.ui.listWidget.addItem("beta °/rad error : betarad={} beta en rad={}".format(self.Arrondi(betarad,cs),self.Arrondi(beta*math.pi/180,cs)))

        # check cohérence alpha° / beta°
        if alpha != 0 and beta != 0 and abs(self.Arrondi(alpha+beta,cs)-90.000) >= 1/10**cs:
            self.clear0()
            return self.ui.listWidget.addItem("alpha beta ° error : alpha+beta={}°".format(alpha+beta))

        # check cohérence alpha rad / beta rad
        if alpharad != 0 and betarad != 0 and abs(self.Arrondi(betarad+alpharad,cs)-self.Arrondi(math.pi/2,cs)) >=1/10**cs:
            self.clear0()
            return self.ui.listWidget.addItem("alpha beta rad error : betarad+alpharad={} pi/2={}".format(self.Arrondi(betarad+alpharad,cs),self.Arrondi(math.pi/2,cs)))

        #superpose angles and convert them in rad unit
        if alpharad == 0:
            alphap=alpha*math.pi/180
        else:
            alphap=alpharad
        if betarad == 0:
            betap=beta*math.pi/180
        else:
            betap=betarad

         # check cohérence alphap rad / betap rad
        if alphap != 0 and betap != 0 and abs(self.Arrondi(betap+alphap,cs)-self.Arrondi(math.pi/2,cs)) >= 1/10**cs:
            self.clear0()
            return self.ui.listWidget.addItem("alpha beta error : beta+alpha={} pi/2={}".format(self.Arrondi(betap+alphap,cs),self.Arrondi(math.pi/2,cs)))

        # check cohérence AB > AC/BC
        if AB != 0 and AC != 0 and AB < AC:
            self.clear0()
            return self.ui.listWidget.addItem("AB AC error : AB={} should > AC={}".format(AB,AC))
        if AB != 0 and BC != 0 and AB < BC:
            self.clear0()
            return self.ui.listWidget.addItem("AB BC error : AB={} should > BC={}".format(AB,BC))

        # check cohérence angle lenght
        if alphap != 0:
            if BC != 0 and AC != 0:
                if abs(self.Arrondi(math.tan(alphap),cs)-self.Arrondi(BC/AC,cs)) >= 1.1/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("alpha BC AC error : tan(alpha)={} BC/AC={}".format(self.Arrondi(math.tan(alphap),cs),self.Arrondi(BC/AC,cs)))
            if BC != 0 and AB != 0:
                if abs(self.Arrondi(math.sin(alphap),cs)-self.Arrondi(BC/AB,cs)) >= 1/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("alpha BC AB error : sin(alpha)={} BC/AB={}".format(self.Arrondi(math.sin(alphap),cs),self.Arrondi(BC/AB,cs)))
            if AC != 0 and AB != 0:
                if abs(self.Arrondi(math.cos(alphap),cs)-self.Arrondi(AC/AB,cs)) >= 1/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("alpha AC AB error : cos(alpha)={} AC/AB={}".format(self.Arrondi(math.cos(alphap),cs),self.Arrondi(AC/AB,cs)))
        if betap != 0:
            if AC != 0 and BC != 0:
                if abs(self.Arrondi(math.tan(betap),cs)-self.Arrondi(AC/BC,cs)) >= 1.2/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("beta AC BC error : tan(beta)={} AC/BC={}".format(self.Arrondi(math.tan(betap),cs),self.Arrondi(AC/BC,cs)))
            if AB != 0 and BC != 0:
                if abs(self.Arrondi(math.cos(betap),cs)-self.Arrondi(BC/AB,cs)) >= 1/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("beta BC AB error : cos(beta)={} BC/AB={}".format(self.Arrondi(math.cos(betap),cs),self.Arrondi(BC/AB,cs)))
            if AB != 0 and AC != 0:
                if abs(self.Arrondi(math.sin(betap),cs)-self.Arrondi(AC/AB,cs)) >= 1/10**cs:
                    self.clear0()
                    return self.ui.listWidget.addItem("beta AC AB error : sin(beta)={} AC/AB={}".format(self.Arrondi(math.sin(betap),cs),self.Arrondi(AC/AB,cs)))

        # check cohérence AB AC BC
        if AB != 0 and AC != 0 and BC != 0:
            if abs(self.Arrondi(AB*AB,cs)-self.Arrondi(AC*AC+BC*BC,cs)) >= 1.1/10**cs:
                return self.ui.listWidget.addItem("AB AC BC error : AB²={} AC²+BC²={}".format(self.Arrondi(AB*AB,cs),self.Arrondi(AC*AC+BC*BC,cs)))
            else:
                return self.ui.listWidget.addItem("no calcul needed")

        if AB+AC+BC==0:
            # no lenght given
            self.ui.listWidget.addItem("Enter atleast 1 lenght")
            self.clear0()
        else:
            if AB+AC==0 or AB+BC==0 or AC+BC==0:
                # 1 lenght given
                if betap+alphap==0:
                    # 0 angle given
                    self.ui.listWidget.addItem("Enter atleast 2 lenght or 1 angle and 1 lenght")
                    self.clear0()
                else:
                    # print("1")
                    self.Calculer()
            else:
                # 2 or 3 lenght given
                self.Calculer()
                # print("2")
    # calcule
    def Calculer(self):

        #import all LineEdit
        AB=float(self.ui.AB.text())
        AC=float(self.ui.AC.text())
        BC=float(self.ui.BC.text())
        alpha=float(self.ui.alpha.text())
        beta=float(self.ui.beta.text())
        alpharad=float(self.ui.alpha_rad.text())
        betarad=float(self.ui.beta_rad.text())
        cs=int(self.ui.ChiffreSign.text())

        #superpose angles and convert them in rad unit
        if alpharad == 0:
            alphap=alpha*math.pi/180
        else:
            alphap=alpharad

        if betarad == 0:
            betap=beta*math.pi/180
        else:
            betap=betarad

        #create lenght "provisoire"
        ABp=AB
        ACp=AC
        BCp=BC

        #calculate lenght with angles if it's possible
        if alphap != 0:
            if AC != 0 and AB == 0:
                ABp=AC/math.cos(alphap)
                self.ui.listWidget.addItem("AB={} calculate with AC/cos(alpha)".format(self.Arrondi(ABp,cs)))
            if BC != 0 and AB == 0:
                ABp=BC/math.sin(alphap)
                self.ui.listWidget.addItem("AB={} calculate with BC/sin(alpha)".format(self.Arrondi(ABp,cs)))
            if AB != 0 and AC == 0:
                ACp=AB*math.cos(alphap)
                self.ui.listWidget.addItem("AC={} calculate with AB*cos(alpha)".format(self.Arrondi(ACp,cs)))
        if betap != 0:
            if AC != 0 and AB == 0:
                ABp=AC/math.sin(betap)
                self.ui.listWidget.addItem("AB={} calculate with AC/sin(beta)".format(self.Arrondi(ABp,cs)))
            if BC != 0 and AB == 0:
                ABp=BC/math.cos(betap)
                self.ui.listWidget.addItem("AB={} calculate with BC/cos(beta)".format(self.Arrondi(ABp,cs)))
            if AB != 0 and BC == 0:
                BCp=AB*math.cos(betap)
                self.ui.listWidget.addItem("BC={} calculate with AB*cos(beta)".format(self.Arrondi(BCp,cs)))

        #refresh lenght's value 
        AB=ABp
        AC=ACp
        BC=BCp
        
        #calcutate lenghts with lenght if neened
        if AC != 0 and BC != 0 and AB == 0:
            ABp=math.sqrt(AC*AC+BC*BC)
            self.ui.listWidget.addItem("AB={} calculate with sqrt(AC²+BC²))".format(self.Arrondi(ABp,cs)))
        if AB != 0 and BC != 0 and AC == 0:
            ACp=math.sqrt(AB*AB-BC*BC)
            self.ui.listWidget.addItem("AC={} calculate with sqrt(AB²-BC²))".format(self.Arrondi(ACp,cs)))
        if AB != 0 and AC != 0 and BC == 0:
            BCp=math.sqrt(AB*AB-AC*AC)
            self.ui.listWidget.addItem("BC={} calculate with sqrt(AB²-AC²))".format(self.Arrondi(BCp,cs)))
            
        #refresh lenght's value
        AB=ABp
        AC=ACp
        BC=BCp

        #calculate angle with lenght if needed
        if AB != 0 and (AC != 0 or BC != 0) :
            if alpha == 0:
                alpha=math.acos(AC/AB)*180/math.pi
                self.ui.listWidget.addItem("alpha={} calculate with arccos(AC/AB) * 180/pi".format(self.Arrondi(alpha,cs)))
            if beta == 0:
                beta=math.acos(BC/AB)*180/math.pi
                self.ui.listWidget.addItem("beta={} calculate with arccos(BC/AB) * 180/pi".format(self.Arrondi(beta,cs)))
            if alpharad == 0:
                alpharad=math.acos(AC/AB)
                self.ui.listWidget.addItem("alpharad={} calculate with arccos(AC/AB)".format(self.Arrondi(alpharad,cs)))
            if betarad == 0:
                betarad=math.acos(BC/AB)
                self.ui.listWidget.addItem("betarad={} calculate with arccos(BC/AB)".format(self.Arrondi(betarad,cs)))

        #round values
        AB=self.Arrondi(AB,cs)
        AC=self.Arrondi(AC,cs)
        BC=self.Arrondi(BC,cs)
        alpha=self.Arrondi(alpha,cs)
        beta=self.Arrondi(beta,cs)
        alpharad=self.Arrondi(alpharad,cs)
        betarad=self.Arrondi(betarad,cs)
        
        #show values in LineEdit
        self.ui.AB.setText(str(AB))
        self.ui.AC.setText(str(AC))
        self.ui.BC.setText(str(BC))
        self.ui.alpha.setText(str(alpha))
        self.ui.beta.setText(str(beta))
        self.ui.alpha_rad.setText(str(alpharad))
        self.ui.beta_rad.setText(str(betarad))

        self.ui.listWidget.addItem("return AB={} / AC={} / BC={} / alpha={} / beta={} / alpharad={} / betarad={}".format(AB,AC,BC,alpha,beta,alpharad,betarad))
 
    # suppport module round
    def Arrondi(self,a,b):
        ap=a*(10**b)
        if ap-int(ap) >= 0.5:
            return (int(ap)+1)/(10**b)
        else:
            return int(ap)/(10**b)

    # support module clear 0 from lineEdit
    def clear0(self):
        if self.ui.AB.text() == "0":
            self.ui.AB.setText("")
        if self.ui.AC.text() == "0":
            self.ui.AC.setText("")
        if self.ui.BC.text() == "0":
            self.ui.BC.setText("")
        if self.ui.alpha.text() == "0":
            self.ui.alpha.setText("")
        if self.ui.beta.text() == "0":
            self.ui.beta.setText("")
        if self.ui.alpha_rad.text() == "0":
            self.ui.alpha_rad.setText("")
        if self.ui.beta_rad.text() == "0":
            self.ui.beta_rad.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main()
    sys.exit(app.exec_())
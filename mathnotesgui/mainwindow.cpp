#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{    
    ui->setupUi(this);

    euler = new Euler();
    connect(euler, SIGNAL(receivedMathString(int, int, QString)), this, SLOT(receivedMathString(int, int, QString)));

    renderer = new Renderer();

    // Create tabs
    tabs = new QTabWidget(this);
    tabs->setDocumentMode(true);
    tabs->setTabsClosable(true);
    tabs->setMovable(true);
    ui->container->layout()->addWidget(tabs);
    createNewTab();

    // Create Command panel
    cmdpanel = new CmdPanel(this);
    ui->container->layout()->addWidget(cmdpanel);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::closeEvent(QCloseEvent *e) {
    if (isWindowModified()) {
        QMessageBox msgBox;
        msgBox.setText("The document has been modified.");
        msgBox.setInformativeText("Do you want to save your changes?");
        msgBox.setStandardButtons(QMessageBox::Save | QMessageBox::Discard | QMessageBox::Cancel);
        msgBox.setDefaultButton(QMessageBox::Save);
        int ret = msgBox.exec();
        if (ret == QMessageBox::Save) saveFile();
        else if (ret == QMessageBox::Cancel) e->ignore();
        else if (ret == QMessageBox::Discard) {
            setWindowModified(false);
        }
    } else {
        euler->terminate();
        qDebug() << "Terminate python.";
    }
}

// Tabs

void MainWindow::createNewTab(bool empty, QString fileName)
{
    QFrame *contents = new QFrame();
    contents->setLayout(new QVBoxLayout());
    contents->layout()->setAlignment(Qt::AlignTop);
    contents->setBackgroundRole(QPalette::Light);
    contents->setFocusPolicy(Qt::NoFocus);

    QScrollArea *scrollArea = new QScrollArea();
    scrollArea->setWidget(contents);
    scrollArea->setWidgetResizable(true);
    scrollArea->setFocusPolicy(Qt::NoFocus);

    tabs->addTab(scrollArea, fileName);
    tabs->setCurrentWidget(scrollArea);
    connect(tabs, SIGNAL(tabBarClicked(int)), this, SLOT(onTabChange(int)));
    setWindowTitle("iEuler - "+fileName);

    numberOfLines = 0;
    if (!empty) addNewParagraph();
}


void MainWindow::addNewParagraph(QString mathString)
{
    Paragraph *paragraph = new Paragraph(this,
                                         euler,
                                         renderer,
                                         tabs->currentIndex(),
                                         numberOfLines,
                                         mathString);

    getTabContents()->layout()->addWidget(paragraph);
    connect(paragraph, SIGNAL(changeFocus_triggered(bool,int)), this, SLOT(changeFocus_triggered(bool,int)));
    connect(paragraph, SIGNAL(newLine_triggered(int)), this, SLOT(newLine_triggered(int)));
    connect(paragraph, SIGNAL(deleteLine_triggered(Paragraph*)), this, SLOT(deleteLine_triggered(Paragraph*)));

    numberOfLines++;
    paragraph->focus();
}

void MainWindow::newLine_triggered(int index)
{
    if (index == numberOfLines - 1) {
        addNewParagraph();
    }
}

void MainWindow::deleteLine_triggered(Paragraph *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
        getTabContents()->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}


// File I/O

void MainWindow::openFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getOpenFileName(this,
        tr("Open iEuler file"), dir, tr("Text Files (*.euler)"));
    if (path != "") {
        QFileInfo fi(path);
        createNewTab(true, fi.fileName());

        euler->sendOpenFileRequest(path);
    }

}

void MainWindow::saveFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Save iEuler file"), dir, tr("Text Files (*.euler)"));

    if (path != "") {
        euler->sendSaveFileRequest(path);
    }
}

void MainWindow::exportFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Export PDF file"), dir, tr("PDF Files (*.pdf)"));

    if (path != "") {
        euler->sendExportRequest(path);
    }
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::changeFocus_triggered(bool up, int index)
{
    if (up) {
        if (index > 0) focusPreviousChild();
    } else {
        if (index < numberOfLines-1) focusNextChild();
    }
}

void MainWindow::keyPressEvent(QKeyEvent *e)
{
    if (e->key() == Qt::Key_Escape) {
        cmdpanel->hide();
    }
}

void MainWindow::receivedMathString(int tabIndex, int index, QString mathString)
{
    addNewParagraph(mathString);
}

void MainWindow::on_action100_triggered()
{
    renderer->setZoomFactor(1);
}

void MainWindow::on_action150_triggered()
{
    renderer->setZoomFactor(1.5);
}

void MainWindow::on_action200_triggered()
{
    renderer->setZoomFactor(2);
}

void MainWindow::on_actionNew_triggered()
{
    createNewTab();
}

void MainWindow::on_actionClose_triggered()
{
    if (tabs->currentIndex() > 0) {
        tabs->setCurrentIndex(tabs->currentIndex() - 1);
        tabs->removeTab(tabs->currentIndex() + 1);
    }
}

QWidget* MainWindow::getTabContents() {
    return ((QScrollArea*) tabs->currentWidget())->widget();
}

void MainWindow::on_actionOpen_triggered()
{
    openFile();
}

void MainWindow::on_actionSave_triggered()
{
    saveFile();
}

void MainWindow::on_actionExport_triggered()
{
    exportFile();
}

void MainWindow::onTabChange(int index)
{
    setWindowTitle("iEuler - "+tabs->tabText(index));
}

void MainWindow::on_actionRestart_core_triggered()
{
    euler->restartCore();
}

#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{    
    ui->setupUi(this);
    initSubprocess();
    MathRenderer::initRenderer();


    loadingMode = false;

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
    if (!empty) createGroup();
}


// Groups

void MainWindow::createGroup(QString cmd)
{
    Group* gp = new Group(this, numberOfLines);
    getTabContents()->layout()->addWidget(gp);
    connect(gp->input, SIGNAL(previewCode(CodeInput*, QString)), this, SLOT(previewCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(evaluateCode(CodeInput*, QString)), this, SLOT(evaluateCode(CodeInput*, QString)));
    connect(gp->input, SIGNAL(deleteGroup(QWidget*)), this, SLOT(deleteGroup(QWidget*)));
    connect(gp->input, SIGNAL(arrowsPressed(bool)), this, SLOT(arrowsPressed(bool)));
    connect(this, SIGNAL(outputReady(int, QString)), gp, SLOT(outputReady(int, QString)));
    numberOfLines++;
    gp->input->setPlainText(cmd);
    gp->input->setFocus();
}

void MainWindow::deleteGroup(QWidget *target)
{
    if (numberOfLines > 1) {
        focusPreviousChild();
         getTabContents()->layout()->removeWidget(target);
        delete target;
        numberOfLines--;
    }
}

// IO

void MainWindow::initSubprocess()
{
    proc = new QProcess(this);
    proc->start("./python3 start.py -gui");
    connect(proc, SIGNAL(readyReadStandardOutput()), this, SLOT(readStandardOutput()));
    connect(proc, SIGNAL(readyReadStandardError()), this, SLOT(readStandardError()));
}

void MainWindow::readStandardOutput()
{
    while (proc->canReadLine()) {
        QString cmdInput = QString::fromLocal8Bit(proc->readLine());

        if (!loadingMode) {
            // get line index and latex string from iEuler
            int split = cmdInput.indexOf(' ');
            int index = cmdInput.left(split).toInt();
            QString latexString = cmdInput.mid(split + 1);
            latexString = latexString.replace("\n", "");
             if (index > numberOfLines - 1) {
                 createGroup();
             }
            // send signal to render math
            emit outputReady(index, latexString);
        } else if (cmdInput == "Done\n") {
            loadingMode = false;
        } else {
            int split = cmdInput.indexOf(' ');
    //        int index = cmdInput.left(split).toInt();
            QString cmdString = cmdInput.mid(split + 1);
            cmdString = cmdString.replace("\n", "");
            createGroup(cmdString);
        }
    }
}

void MainWindow::readStandardError()
{
    qDebug() << "python error: \n" << proc->readAllStandardError();
}

void MainWindow::previewCode(CodeInput* target, QString inputString)
{
    QString index = QString::number(((Group*) target->parent())->index);
    inputString = inputString.replace('\n',' ');

    proc->write(index.toLatin1()+"\n");
    proc->write("preview\n");
    proc->write(inputString.toLatin1()+"\n");
//    setWindowModified(true);
}

void MainWindow::evaluateCode(CodeInput* target, QString inputString)
{
    QString index = QString::number(((Group*) target->parent())->index);
    inputString = inputString.replace('\n',' ');

    proc->write(index.toLocal8Bit()+"\n");
    proc->write("evaluate\n");
    proc->write(inputString.toLocal8Bit()+"\n");
    if (((Group*) target->parent())->index == numberOfLines-1) {
        createGroup();
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
        loadingMode = true;
        proc->write("load\n");
        proc->write(path.toLocal8Bit()+"\n");
    }
}

void MainWindow::saveFile()
{
    QString dir = QStandardPaths::locate(QStandardPaths::DocumentsLocation, QString(), QStandardPaths::LocateDirectory);
    QString path = QFileDialog::getSaveFileName(this,
        tr("Save iEuler file"), dir, tr("Text Files (*.euler)"));
    proc->write("save\n");
    proc->write(path.toLocal8Bit()+"\n");
}

void MainWindow::exportFile()
{
    proc->write("export\n");
}

void MainWindow::on_actionShow_command_panel_triggered()
{
    if (cmdpanel->isVisible()) {
        cmdpanel->hide();
    } else {
        cmdpanel->show();
    }
}

void MainWindow::arrowsPressed(bool upArrowPressed)
{
    int index = ((Group*) focusWidget()->parent())->index;
    if (upArrowPressed) {
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

void MainWindow::on_action100_triggered()
{
    MathRenderer::zoomFactor = 1;
}



void MainWindow::on_action150_triggered()
{
    MathRenderer::zoomFactor = 1.5;
}

void MainWindow::on_action200_triggered()
{
    MathRenderer::zoomFactor = 2;
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

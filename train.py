from analyzer.ml_model import EmailClassifier
clf = EmailClassifier(model_path='./models/nb_model.joblib')
res = clf.train_from_csv('./sample_emails_1k.csv')
print('Training finished. Accuracy:', res.get('accuracy'))
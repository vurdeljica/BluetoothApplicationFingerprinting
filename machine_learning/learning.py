import fs_util
import paths
import pandas as pd
import os

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report
from sklearn.model_selection import KFold # import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
#import xlsxwriter
from util import paths
from util import fs_util

class Learning:
    def __init__(self):
        self.__source = paths.RESULT_DIR
        self.__destination = paths.LEARNING_RESULT_DIR
        fs_util.delete_directory(paths.LEARNING_RESULT_DIR)

    def __check_source_validity(self):
        is_source_dir_present = fs_util.check_if_directory_exists(self.__source)
        if not is_source_dir_present:
            print("Source directory path is not valid")
            return False

        if fs_util.check_if_directory_exists(self.__destination):
            is_destination_deleted = fs_util.delete_directory(self.__destination)
            if not is_destination_deleted:
                print("Couldn't delete: " + self.__destination)
                return False

        is_destination_created = fs_util.make_directory(self.__destination)
        if not is_destination_created:
            print("Couldn't make destination directory: " + self.__destination)
            return False

        #input_data_directory_paths = fs_util.get_list_of_subdirectory_paths(self.__source)
        #for input_data_directory_path in input_data_directory_paths:
            #application_result_dir_path = os.path.join(paths.LEARNING_RESULT_DIR,
            #                                           fs_util.get_name_from_path(input_data_directory_path))
            #is_destination_created = fs_util.make_directory(application_result_dir_path)
            #if not is_destination_created:
            #    print("Couldn't make application directory: " + application_result_dir_path)
            #    return False

        return True

    """def __generate_signature(self, src_dir_path, file_path):
        dst_dir_path = os.path.join(paths.LEARNING_RESULT_DIR, fs_util.get_name_from_path(src_dir_path))

        data_frame = pd.read_csv(file_path)

        inter_arrival_times_ms = np.array(data_frame['inter_arrival_time'])

        plot_path = os.path.join(dst_dir_path,
                                 fs_util.get_name_from_path(fs_util.get_file_name_without_extension(file_path)))
        sns.distplot(inter_arrival_times_ms)
        plt.savefig(plot_path)
        plt.clf()

        bins = [5 * index for index in range(2000)]
        plot_path = os.path.join(dst_dir_path,
                                 fs_util.get_name_from_path(fs_util.get_file_name_without_extension(file_path)) + "2")
        plt.hist(inter_arrival_times_ms, bins=bins)
        #plt.savefig(plot_path)
        plt.clf()
    """

    def __get_summarized_application_log(self, file_path):
        df = pd.read_csv(file_path)
        return df

    def __generate_learning_data_set(self):
        input_data_directory_paths = fs_util.get_list_of_subdirectory_paths(self.__source)
        data_set = None

        for input_data_directory_path in input_data_directory_paths:
            file_paths_in_directory = fs_util.get_list_of_file_paths_in_directory(input_data_directory_path)
            for file_path in file_paths_in_directory:
                label = fs_util.get_name_from_path(input_data_directory_path)
                data_frame = self.__get_summarized_application_log(file_path)
                data_frame['label'] = [label]

                if data_set is not None:
                    data_set = data_set.append(data_frame)
                else:
                    data_set = data_frame

        data_set.to_csv(os.path.join(paths.LEARNING_RESULT_DIR, 'dataset.csv'), index=False)

        return data_set

    def __calc_accuracy(self, classifier, X, y):
        num_of_splits = 5
        n_repeats = 10
        kf = RepeatedStratifiedKFold(n_splits=num_of_splits, n_repeats=n_repeats)  # Define the split - into 2 folds
        average_accuracy = 0.0

        original_class = []
        predicted_class = []

        for train_index, test_index in kf.split(X, y):
            X_train = X.iloc[train_index]
            X_test = X.iloc[test_index]
            y_train = y[train_index]
            y_test = y[test_index]

            classifier.fit(X_train, y_train)
            average_accuracy += classifier.score(X_test, y_test)

            y_pred = classifier.predict(X_test)
            #print('Accuracy of classifier on test set: {:.2f}'.format(classifier.score(X_test, y_test)))
            #print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
            #                                                         'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
            #                                                          'TicTacToe', 'TwoGuysAndZombies',
            #                                                          'VirtualTableTennis', 'Warlings']))

            original_class.extend(y_test)
            predicted_class.extend(y_pred)

        average_accuracy /= (num_of_splits * n_repeats)
        print('Average accuracy of the', classifier.__class__.__name__, 'is: {:.4f}'.format(average_accuracy))
        print(classification_report(original_class, predicted_class, digits=4,
                                    target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                  'VirtualTableTennis', 'Warlings']))

        report_dict = classification_report(original_class, predicted_class, digits=4,
                                    target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                  'VirtualTableTennis', 'Warlings'],
                                    output_dict=True)
        report_dict_pd = pd.DataFrame(report_dict)
        report_dict_pd = report_dict_pd.transpose()
        report_dict_pd.pop('support')
        report_dict_pd = report_dict_pd.apply(lambda x: x * 100.0)
        report_dict_pd = report_dict_pd.round(decimals=2)
        report_dict_pd.to_csv(os.path.join(paths.LEARNING_RESULT_DIR, classifier.__class__.__name__ + '.csv'))
        #return report_dict_pd
        #print(pd.DataFrame(report_dict))
        #pd.DataFrame(report_dict)

    def __learn(self, data_set):
        X = data_set.loc[:, data_set.columns != 'label']
        y = pd.Categorical(data_set['label']).codes

        logreg = LogisticRegression(solver='lbfgs', multi_class='ovr', max_iter=1000)
        knn = KNeighborsClassifier(n_neighbors=3)
        clf = RandomForestClassifier(n_estimators=50)
        nb = GaussianNB()
        svm_poly = SVC(kernel='poly', gamma='auto', degree=3, C=1, decision_function_shape='ovo')

        models = [logreg, knn, clf, nb, svm_poly]
        for model in models:
            self.__calc_accuracy(model, X, y)

        result_paths = []
        file_labels = []
        destination_path = os.path.join(paths.LEARNING_RESULT_DIR, "complete_table.csv")
        for model in models:
            result_file_path = os.path.join(paths.LEARNING_RESULT_DIR, model.__class__.__name__ + '.csv')
            file_labels.append(model.__class__.__name__)
            result_paths.append(result_file_path)

        fs_util.merge_multiple_csv_files(result_paths, file_labels, destination_path)

        #importance = logreg.coef_[0]
        # summarize feature importance
        #for i, v in enumerate(importance):
        #    print('Feature: %0d, Score: %.5f' % (i, v))

    """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify = y)
        logreg = LogisticRegression(solver='lbfgs', multi_class='ovr')

        logreg.fit(X_train, y_train)
        y_pred = logreg.predict(X_test)

        print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
        print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                                  'VirtualTableTennis', 'Warlings']))

        knn = KNeighborsClassifier(n_neighbors=3)
        knn_model_1 = knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        print('k-NN accuracy for test set: %f' % knn_model_1.score(X_test, y_test))
        print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                                  'VirtualTableTennis', 'Warlings']))

        clf = RandomForestClassifier(n_estimators=10)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        print('Random forest accuracy for test set: %f' % clf.score(X_test, y_test))
        print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                                  'VirtualTableTennis', 'Warlings']))

        nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                           hidden_layer_sizes=(5, 2), random_state=1)
        nn.fit(X, y)
        y_pred = nn.predict(X_test)
        print('NN MLPClassifier accuracy for test set: %f' % nn.score(X_test, y_test))
        print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                                  'VirtualTableTennis', 'Warlings']))

        model = GaussianNB()
        model.fit(X, y)
        y_pred = model.predict(X_test)
        print('GaussianNB accuracy for test set: %f' % model.score(X_test, y_test))
        print(classification_report(y_test, y_pred, target_names=['4InARow', 'BluetoothShooter', 'Domino',
                                                                  'HitThePlane', 'LudoClassic', 'SnakesAndLadders',
                                                                  'TicTacToe', 'TwoGuysAndZombies',
                                                                  'VirtualTableTennis', 'Warlings']))
    """
    def start(self):
        if not self.__check_source_validity():
            return

        data_set = self.__generate_learning_data_set()
        self.__learn(data_set)

    def show_file_statistic(self, filepath):
        raise NotImplemented

    def show_overall_statistics(self):
        raise NotImplemented

    def set_source(self, source_path):
        self.__source = source_path

    def set_destination(self, destination_path):
        self.__destination = destination_path

#include <iostream>
#include <vector>
#include <limits>
#include <fstream>
#include "json.hpp"


using namespace std;
using json = nlohmann::json;

json weight_map = NULL;
bool weighted = false;

long minimum(long left, long right){
    if (left<right) return left;
    else return right;

}

double minimum(vector<double>* nmbrs){
    double  min = numeric_limits<double>::max();
    for ( auto &i : *nmbrs ){
        if(i < min){
            min = i;
        }
        if (min == 0) {
            return min;
        }
    }
    return min;
}

long maximum(long left, long right){
    if (left>right) return left;
    else return right;
}

json load_weights(string path){
    std::ifstream weights_file(path);
    weights_file >> weight_map;
}

double calc_weight(char ch_a, char ch_b){
    string a, b;
    a = string(1, ch_a);
    b = string(1, ch_b);
    if (a == b) return 0.0;
    if (!weighted) return 1.0;
    try{
        return weight_map[a+b];
    }
    catch (domain_error) {
        try {
            return weight_map[b + a];
        }
        catch (domain_error){
            return 1.0;
        }
    }
}

double damerau_levenshtein(string* left, string* right, unsigned long l_len, unsigned long r_len){

    if (minimum(l_len, r_len) == 0){
        return maximum(l_len, r_len);
    }

    unsigned long r_final_char_idx = r_len - 1;
    unsigned long l_final_char_idx = l_len - 1;

    double weight = calc_weight(left->at(l_final_char_idx), right->at(r_final_char_idx));



    vector<double> vals;

    if (( l_len > 1 and  r_len > 1) and
        (left->at(l_final_char_idx) == right->at(r_final_char_idx - 1)) and
        (left->at(l_final_char_idx -1 ) == right->at(r_final_char_idx))) {


        vals.push_back(damerau_levenshtein(left, right, l_len -1 , r_len) + weight);
        vals.push_back(damerau_levenshtein(left, right, l_len, r_len - 1) + weight);
        vals.push_back(damerau_levenshtein(left, right , l_len - 1, r_len - 1) + weight);
        vals.push_back(damerau_levenshtein(left, right , l_len - 2, r_len - 2) + weight);
        return minimum(&vals);
    }
    else{
        vals.push_back(damerau_levenshtein(left, right, l_len - 1, r_len) + weight);
        vals.push_back(damerau_levenshtein(left, right, l_len, r_len - 1) + weight);
        vals.push_back(damerau_levenshtein(left, right, l_len - 1, r_len - 1) + weight);
        return minimum(&vals);
    }
}


int main(int argc, char* argv[]) {

    if (argc >= 4) {
        string mode, left, right;
        mode = string(argv[1]);
        left = string(argv[2]);
        right = string(argv[3]);

        if (mode.compare("weighted") == 0){
            weighted = true;
            string weightsfile;
            if (argc == 5){
                weightsfile = string(argv[4]);
            }
            else{
                cout<<"Missing weightsfile" <<endl;
                return -1;
            }
            load_weights(weightsfile);
            double dist = damerau_levenshtein(&left, &right, left.length(), right.length());
            cout << "The weighted damerau levenshtein distance between " + left + " and " + right + " is " + to_string(dist) <<endl;
            return 0;
        }
        else if(mode.compare("unweighted") == 0){
            int dist = damerau_levenshtein(&left, &right, left.length(), right.length());
            cout << "The damerau levenshtein distance between " + left + " and " + right + " is " + to_string(dist) <<endl;
            return 0;
        }
        else{
            cout << "Given mode must be one of [weighted|unweighted]"<<endl;
            return -1;
        }
        return 0;
    } else {
        cout << "Call must be \"./levenshtein-c weighted|unweighted string1 string2 [weightsfile]\"" << endl;
        return -1;
    }
}
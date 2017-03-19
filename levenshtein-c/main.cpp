#include <iostream>
#include <vector>
#include <limits>
#include <fstream>
#include "json.hpp"


using namespace std;
using json = nlohmann::json;


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

double damerau_levenshtein(string* left, string* right, unsigned long l_final_char_idx, unsigned long r_final_char_idx){

    if (minimum(l_final_char_idx, r_final_char_idx) == 0){
        return maximum(l_final_char_idx, r_final_char_idx);
    }


    vector<double> vals;

    if (( l_final_char_idx > 1 and  r_final_char_idx > 1) and
            (left->at(l_final_char_idx) == right->at(r_final_char_idx - 1)) and
            (left->at(l_final_char_idx -1 ) == right->at(r_final_char_idx))) {


        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx -1 , r_final_char_idx) + 1);
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx, r_final_char_idx - 1) + 1);
        if (left->at(l_final_char_idx) == right->at(r_final_char_idx)) {
            vals.push_back(damerau_levenshtein(left, right , l_final_char_idx - 1, r_final_char_idx - 1));
        }
        else{
            vals.push_back(damerau_levenshtein(left, right , l_final_char_idx - 1, r_final_char_idx - 1) + 1);
        }
        vals.push_back(damerau_levenshtein(left, right , l_final_char_idx - 2, r_final_char_idx - 2) + 1);
        return minimum(&vals);
    }
    else{
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx) + 1);
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx, r_final_char_idx - 1) + 1);
        if (left->at(l_final_char_idx) == right->at(r_final_char_idx)) {
            vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx - 1));
        }
        else {
            vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx - 1) + 1);

        }
        return minimum(&vals);
    }
}

json load_weights(string path){
    std::ifstream weights_file(path);
    json weight_map;
    weights_file >> weight_map;
    return weight_map;
}

double calc_weight(json* weight_map, string a, string b){
    if (a == b) return 0.0;
    try{
        return weight_map->operator[](a+b);
    }
    catch(domain_error e){
        try{
            return weight_map->operator[](b+a);
        }
        catch(domain_error e){
            return 1.0;
        }
    }
}

double damerau_levenshtein_weighted(json* weight_map, string* left, string* right, double l_final_char_idx, double r_final_char_idx){

    if (minimum(l_final_char_idx, r_final_char_idx) == 0){
        return maximum(l_final_char_idx, r_final_char_idx);
    }


    vector<double> vals;

    if (( l_final_char_idx > 1 and  r_final_char_idx > 1) and
        (left->at(l_final_char_idx) == right->at(r_final_char_idx - 1)) and
        (left->at(l_final_char_idx -1 ) == right->at(r_final_char_idx))) {


        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx -1 , r_final_char_idx) + 1);
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx, r_final_char_idx - 1) + 1);
        vals.push_back(damerau_levenshtein(left, right , l_final_char_idx - 1, r_final_char_idx - 1) + calc_weight());
        vals.push_back(damerau_levenshtein(left, right , l_final_char_idx - 2, r_final_char_idx - 2) + 1);
        return minimum(&vals);
    }
    else{
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx) + 1);
        vals.push_back(damerau_levenshtein(left, right, l_final_char_idx, r_final_char_idx - 1) + 1);
        if (left->at(l_final_char_idx) == right->at(r_final_char_idx)) {
            vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx - 1));
        }
        else {
            vals.push_back(damerau_levenshtein(left, right, l_final_char_idx - 1, r_final_char_idx - 1) + 1);

        }
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
            string weightsfile;
            if (argc == 5){
                weightsfile = string(argv[4]);
            }
            else{
                cout<<"Missing weightsfile" <<endl;
                return -1;
            }
            json weight_map = load_weights(weightsfile);
            double dist = damerau_levenshtein_weighted(&weight_map, &left, &right, left.length() - 1, right.length() - 1);
            cout << "The weighted damerau levenshtein distance between " + left + " and " + right + " is " + to_string(dist) <<endl;
        }
        else if(mode.compare("unweighted") == 0){
            int dist = damerau_levenshtein(&left, &right, left.length() - 1, right.length() - 1);
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
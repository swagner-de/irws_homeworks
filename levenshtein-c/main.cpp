#include <iostream>
#include <vector>

using namespace std;

long minimum(long left, long right){
    if (left<right) return left;
    else return right;

}

int minimum(vector<long>* nmbrs){
    long  min;
    for ( auto &i : *nmbrs ){
        if(min == NULL or i < min){
            min = i;
        }
        if (min == 0) {
            return min;
        }
    }
    return min;
}

int maximum(long left, long right){
    if (left>right) return left;
    else return right;
}

long damerau_levenshtein(string* left, string* right, long l_final_char_idx, long r_final_char_idx){

    if (minimum(l_final_char_idx, r_final_char_idx) == 0){
        return maximum(l_final_char_idx, r_final_char_idx);
    }


    vector<long> vals;

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


int main(int argc, char* argv[]) {

    if (argc == 3) {
        string left, right;
        left = string(argv[1]);
        right = string(argv[2]);

        int dist = damerau_levenshtein(&left, &right, left.length() - 1, right.length() - 1);
        cout << "The damerau levenshtein distance between " + left + " and " + right + " is " + to_string(dist) <<endl;
        return 0;
    } else {
        cout << "Only accepting two arguments" << endl;
        return -1;
    }
}
#include <iostream>
#include <vector>

using namespace std;

long minimum(long left, long right){
    if (left<right) return left;
    else return right;

}

int minimum(vector<long>* nmbrs){
    long*  min;
    for ( auto &i : *nmbrs ){
        if(min == NULL or i < *min){
            min = &i;
        }
        if (*min == 0) {
            return *min;
        }
    }
    return *min;
}

int maximum(long left, long right){
    if (left>right) return left;
    else return right;
}

long damerau_levenshtein(string* left, string* right){

    const long l_len =  left->length();
    const long r_len =  right->length();


    if (minimum(r_len, l_len) == 0){
        return maximum(l_len, r_len);
    }

    vector<long> vals;

    string left_1 = left->substr(0, l_len-1);
    string right_1 = right->substr(0, r_len-1);

    if ((l_len > 1 and r_len > 1) and
            (left->at(l_len-1) == right->at(r_len-2)) and
            (left->at(l_len-2) == right->at(r_len-1))) {
        string left_2 = left->substr(0, l_len-2);
        string right_2 = right->substr(0, r_len-2);

        vals.push_back(damerau_levenshtein(&left_1, right) + 1);
        vals.push_back(damerau_levenshtein(left, &right_1) + 1);
        if (left->at(l_len-1) == right->at(r_len-1)) {
            vals.push_back(damerau_levenshtein(&left_1, &right_1));
        }
        else{
                vals.push_back(damerau_levenshtein(&left_1, &right_1) + 1);

            }
        vals.push_back(damerau_levenshtein(&left_2, &right_2) + 1);
        return minimum(&vals);
    }

    else{
        vals.push_back(damerau_levenshtein(&left_1, right) + 1);
        vals.push_back(damerau_levenshtein(left, &right_1) + 1);
        if (left->at(l_len-1) == right->at(r_len-1)) {
            vals.push_back(damerau_levenshtein(&left_1, &right_1));
        }
        else {
            vals.push_back(damerau_levenshtein(&left_1, &right_1) + 1);

        }
        return minimum(&vals);
    }
}


int main(int argc, char* argv[]) {

    if (argc == 3) {
        string left, right;
        left = string(argv[1]);
        right = string(argv[2]);

        int dist = damerau_levenshtein(&left, &right);
        cout << "The damerau levenshtein distance between " + left + " and " + right + " is " + to_string(dist) <<endl;
        return 0;
    } else {
        cout << "Only accepting two arguments" << endl;
        return -1;
    }
}
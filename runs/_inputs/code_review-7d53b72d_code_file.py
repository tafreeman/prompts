Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction:
Design a data structure in C++ to store information of a grocery store inventory.

### Input:


### Response:
#include <map>
#include <string>

class GroceryStoreInventory {
private:
    std::map<std::string, int> items;
public:
    void addItems(std::string item, int quantity) {
        items[item] = quantity;
    }
    int getQuantity(std::string item) {
        if (items.find(item) != items.end()) {
            return items[item];
        }
        return 0;
    }
};
import java.util.*;

/**
 * 题目：移动0到末尾
 * 难度：Easy
 * 类型：双指针
 * 日期：2026-02-01
 */
class MoveZero {

    public void solution(int [] nums) {
		// 双指针实现 
		// 两个指针，一个指向0,一个指向数字
		// 当数字的index 大于 0 交换
		// 直到数字在最后的index 
		int len = nums.length;
		System.out.println(len);
		int zero = 0;
		int num = 0;
		while (num < len && zero <len) {
			// 指针找位置
			while (nums[num] == 0) {
				num++;
			}
			while (zero != 0) {
				zero++;
			}
			// 交换
			if (num > zero) {
				int tmp = nums[zero];
				nums[zero] = nums[num];
				nums[num] = tmp;
			} else {
				num++;
			}
		}

        System.out.println(Arrays.toString(nums));
    }

    public static void main(String[] args) {
        MoveZero sol = new MoveZero();
		int[] nums = { 1,0,2,0,3,4};
        System.out.println(Arrays.toString(nums));
		sol.solution(nums);
    }
}

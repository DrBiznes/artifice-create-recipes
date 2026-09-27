package dev.jam.artificecreaterecipes;

import java.util.List;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;

/** A plain workpiece: no firearm behavior and no modifier functionality. */
public final class IncompleteItem extends Item {
    public IncompleteItem(Properties properties) {
        super(properties);
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        super.appendHoverText(stack, context, tooltip, flag);
        tooltip.add(Component.translatable("tooltip." + ArtificeCreateRecipes.MOD_ID + ".incomplete")
                .withStyle(ChatFormatting.GRAY));
    }
}

package dev.jam.artificecreaterecipes;

import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.bus.api.IEventBus;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.neoforged.neoforge.registries.DeferredRegister;

/** Registers workpieces; Create handles all recipe processing. */
@Mod(ArtificeCreateRecipes.MOD_ID)
public final class ArtificeCreateRecipes {
    public static final String MOD_ID = "artifice_create_recipes";
    public static final String HEXEREI_ID = "hazens_archaic_hexerei_armaments";

    private static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(MOD_ID);
    private static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MOD_ID);

    static {
        WorkpieceNames.ALL.forEach(name -> ITEMS.registerItem(name, IncompleteItem::new));
        if (ModList.get().isLoaded(HEXEREI_ID)) {
            WorkpieceNames.HEXEREI.forEach(name -> ITEMS.registerItem(name, IncompleteItem::new));
        }
        TABS.register("workpieces", () -> CreativeModeTab.builder()
                .title(Component.translatable("itemGroup." + MOD_ID))
                .icon(() -> ITEMS.getEntries().iterator().next().get().getDefaultInstance())
                .displayItems((parameters, output) -> ITEMS.getEntries().forEach(item -> output.accept(item.get())))
                .build());
    }

    public ArtificeCreateRecipes(IEventBus bus) {
        ITEMS.register(bus);
        TABS.register(bus);
    }
}
